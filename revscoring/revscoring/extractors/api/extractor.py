import logging
from itertools import islice

import mwapi

from . import datasources
from .. import Extractor as BaseExtractor
from ...datasources import Datasource, revision_oriented
from ...dependencies import expand
from ...errors import RevisionNotFound, UserNotFound
from .revision_oriented import Revision
from .util import REV_PROPS, USER_PROPS

logger = logging.getLogger(__name__)


class Extractor(BaseExtractor):
    def __init__(self, session, context=None, cache=None):
        super().__init__(context=context, cache=cache)
        self.session = session
        self.dependents = Datasource("extractor.dependents")

        rev_doc = self.get_rev_doc_by_id(revision_oriented.revision)
        self.revision = Revision(
            revision_oriented.revision, self, rev_doc,
            id_datasource=revision_oriented.revision.id
        )

        # Registers revision_oriented context
        self.update(context=self.revision)

    def get_rev_doc_by_id(self, revision):
        return datasources.RevDocById(revision, self)

    def get_page_creation_rev_doc(self, page):
        return datasources.PageCreationRevDoc(page, self)

    def get_user_info_doc(self, user):
        return datasources.UserInfoDoc(user, self)

    def get_last_user_rev_doc(self, user):
        return datasources.LastUserRevDoc(user, self)

    def extract(self, rev_ids, dependents, context=None, caches=None,
                cache=None, profile=None):
        """
        Extracts a values for a set of
        :class:`~revscoring.dependents.dependent.Dependent` (e.g.
        :class:`~revscoring.features.feature.Feature` or
        :class:`~revscoring.datasources.datasource.Datasource`) for a revision
        or a set of revisions
        :Parameters:
            rev_ids : int | `iterable`
                Either a single rev_id or an `iterable` of rev_ids
            dependents : :class:`~revscoring.dependents.dependent.Dependent`
                A set of dependents to extract values for
            context : `dict` | `iterable`
                A set of call-specific
                :class:`~revscoring.Dependent` to inject
            caches : `dict`
                A rev_id-->cache pairs of call-specific pre-computed values to
                inject
            cache : `dict`
                A set of call-specific pre-computed values to inject for every
                rev_id
            profile : `dict`
                A mapping of :class:`revscoring.Dependent` to `list` of process
                durations for generating the value.  The provided `dict` will
                be modified in-place and new durations will be appended.
        :Returns:
            An generator of extracted values if a single rev_id was provided or
            a genetator of (error, values) pairs where error is `None` if no
            error occured during extraction.
        """
        context = context or {}

        if (caches or cache) is not None:
            logger.debug("Extracting {0} dependents with cache {1}"
                         .format(len(dependents), caches or cache))

        if hasattr(rev_ids, "__iter__"):
            return self._extract_many(rev_ids, dependents, context=context,
                                      caches=caches,
                                      cache=cache, profile=profile)
        else:
            rev_id = rev_ids
            cache = cache if cache is not None else {}
            cache.update((caches or {}).get(rev_id, {}))
            return self._extract(rev_id, dependents, cache=cache,
                                 context=context, profile=profile)

    def _extract_many(self, rev_ids, dependents, context, caches, cache,
                      profile):
        all_dependents = set(expand(dependents))

        caches = caches if caches is not None else {}
        caches.update({rev_id: {} for rev_id in rev_ids
                                  if rev_id not in caches})
        for rev_id, rev_cache in caches.items():
            for dependent, value in (cache or {}).items():
                if dependent not in rev_cache:
                    rev_cache[dependent] = value

        errored = {}

        # Build up caches for data that can be queried in batch
        if self.revision & all_dependents:
            rvprop = set(REV_PROPS)
            if self.revision.text in all_dependents:
                rvprop.add('content')

            # datasource.revision.doc
            revids_to_lookup = []
            for rev_id in rev_ids:
                rev_cache = caches[rev_id]
                if self.revision.doc not in rev_cache:
                    revids_to_lookup.append(
                        rev_cache.get(revision_oriented.revision.id, rev_id))

            logger.info("Batch requesting {0} revision from the API"
                        .format(len(revids_to_lookup)))

            rev_docs = self.get_rev_doc_map(revids_to_lookup, rvprop=rvprop)

            for rev_id in rev_ids:
                lookup_rev_id = caches[rev_id].get(
                    revision_oriented.revision.id, rev_id)
                if lookup_rev_id in rev_docs:
                    caches[rev_id][self.revision.doc] = \
                        rev_docs[lookup_rev_id]
                else:
                    errored[rev_id] = RevisionNotFound(self.revision,
                                                       lookup_rev_id)

            # datasource.revision.parent.doc
            if self.revision.parent & all_dependents:
                parentids_to_lookup = []
                for rev_id, rev_cache in caches.items():
                    if self.revision.doc in rev_cache and \
                       self.revision.parent.doc not in rev_cache:
                        rev_doc = rev_cache[self.revision.doc]
                        parent_id = rev_cache.get(
                            revision_oriented.revision.parent.id,
                            rev_doc.get('parentid'))
                        parentids_to_lookup.append(parent_id)

                logger.info("Batch requesting {0} revision.parent from the API"
                            .format(len(parentids_to_lookup)))
                parent_rev_docs = self.get_rev_doc_map(parentids_to_lookup,
                                                       rvprop=rvprop)

                for rev_id, rev_cache in caches.items():
                    if self.revision.doc in rev_cache and \
                       self.revision.parent.doc not in rev_cache:
                        rev_doc = rev_cache[self.revision.doc]
                        parent_id = rev_cache.get(
                            revision_oriented.revision.parent.id,
                            rev_doc.get('parentid'))

                        if parent_id in parent_rev_docs:
                            rev_cache[self.revision.parent.doc] = \
                                parent_rev_docs[parent_id]
                        elif parent_id == 0:
                            rev_cache[self.revision.parent.doc] = None
                        else:
                            errored[rev_id] = \
                                RevisionNotFound(self.revision.parent,
                                                 parent_id)

            if self.revision.user.info & all_dependents:
                user_texts_to_lookup = set()
                for rev_id, rev_cache in caches.items():
                    if self.revision.doc in rev_cache and \
                       self.revision.user.info.doc not in rev_cache:
                        rev_doc = rev_cache[self.revision.doc]
                        if rev_doc.get('userid', 0) > 0:
                            user_texts_to_lookup.add(rev_doc.get('user'))

                logger.info("Batch requesting {0} revision.user.info from "
                            .format(len(user_texts_to_lookup)) + "the API")
                user_info_docs = self.get_user_doc_map(user_texts_to_lookup,
                                                       usprop=USER_PROPS)

                for rev_id, rev_cache in caches.items():
                    if self.revision.doc in rev_cache and \
                       self.revision.user.info.doc not in rev_cache:
                        rev_doc = rev_cache[self.revision.doc]
                        if rev_doc.get('userid', 0) > 0:
                            user_text = rev_doc.get('user')
                            if user_text in user_info_docs:
                                rev_cache[self.revision.user.info.doc] = \
                                    user_info_docs[user_text]
                            else:
                                errored[rev_id] = \
                                    UserNotFound(self.revision.user, user_text)

        # Now extract dependent values one-by-one
        for rev_id in rev_ids:
            # If an error happened, give up hope
            if rev_id in errored:
                yield errored[rev_id], None
            else:
                # If no error happened, try to solve the other dependencies.
                try:
                    values = self._extract(rev_id, dependents, context=context,
                                           cache=caches[rev_id],
                                           profile=profile)
                    yield None, list(values)
                except Exception as e:
                    yield e, None

    def _extract(self, rev_id, dependents, context, cache, profile):
        all_dependents = set(expand(dependents))

        cache.update({self.revision.id: rev_id,
                      self.dependents: all_dependents})
        return self.solve(dependents, context=context, cache=cache,
                          profile=profile)

    def get_rev_doc_map(self, rev_ids, rvprop={'ids', 'user', 'timestamp',
                                               'userid', 'comment', 'content',
                                               'flags', 'size'}):
        if len(rev_ids) == 0:
            return {}

        logger.debug("Building a map of {0} revisions: {1}"
                     .format(len(rev_ids), rev_ids))
        rev_docs = self.query_revisions_by_revids(rev_ids, rvprop=rvprop)

        return {rd['revid']: rd for rd in rev_docs}

    def query_revisions_by_revids(self, revids, batch=50, **params):
        revids_iter = iter(revids)
        while True:
            batch_ids = list(islice(revids_iter, 0, batch))
            if len(batch_ids) == 0:
                break
            else:
                doc = self.session.get(action='query', prop='revisions',
                                       revids=batch_ids, **params)

                for page_doc in doc['query'].get('pages', {}).values():
                    yield from _normalize_revisions(page_doc)

    def get_user_doc_map(self, user_texts,
                         usprop={'groups', 'registration', 'emailable',
                                 'editcount', 'gender'}):
        if len(user_texts) == 0:
            return {}
        logger.debug("Building a map of {0} user.info.docs"
                     .format(len(user_texts)))
        return {ud['name']: ud
                for ud in self.query_users_by_text(user_texts, usprop=usprop)}

    def query_users_by_text(self, user_texts, batch=50, **params):
        user_texts_iter = iter(user_texts)
        while True:
            batch_texts = list(islice(user_texts_iter, 0, batch))
            if len(batch_texts) == 0:
                break
            else:
                doc = self.session.get(action='query', list='users',
                                       ususers=batch_texts, **params)

                for user_doc in doc['query'].get('users', []):
                    yield user_doc

    def get_user_last_revision(self, user_text, rev_timestamp,
                               ucprop={'ids', 'timestamp', 'comment', 'size'}):
        if user_text is None or rev_timestamp is None:
            return None

        logger.debug("Requesting the last revision by {0} from the API"
                     .format(user_text))
        doc = self.session.get(action="query", list="usercontribs",
                               ucuser=user_text, ucprop=ucprop,
                               uclimit=1, ucdir="older",
                               ucstart=(rev_timestamp - 1))

        rev_docs = doc['query']['usercontribs']

        if len(rev_docs) > 0:
            return rev_docs[0]
        else:
            # It's OK to not find a revision here.
            return None

    def get_page_creation_doc(self, page_id,
                              rvprop={'ids', 'user', 'timestamp', 'userid',
                                      'comment', 'flags', 'size'}):
        if page_id is None:
            return None

        logger.debug("Requesting creation revision for ({0}) from the API"
                     .format(page_id))
        doc = self.session.get(action="query", prop="revisions",
                               pageids=page_id, rvdir="newer", rvlimit=1,
                               rvprop=rvprop)

        page_doc = doc['query'].get('pages', {'revisions': []}).values()
        rev_docs = page_doc['revisions']

        if len(rev_docs) == 1:
            return rev_docs[0]
        else:
            # This is bad, but it should be handled by the calling funcion
            return None

    @classmethod
    def from_config(cls, config, name, section_key="extractors"):
        logger.info("Loading api.Extractor '{0}' from config.".format(name))
        section = config[section_key][name]
        kwargs = {k: v for k, v in section.items() if k != "class"}
        return cls(mwapi.Session(**kwargs))


def _normalize_revisions(page_doc):
    page_meta = {k: v for k, v in page_doc.items()
                 if k != 'revisions'}
    if 'revisions' in page_doc:
        for revision_doc in page_doc['revisions']:
            revision_doc['page'] = page_meta
            yield revision_doc
