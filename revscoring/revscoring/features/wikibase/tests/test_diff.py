import json
import os
import pickle

from nose.tools import eq_

from ....dependencies import solve
from ..revision_oriented import revision

pwd = os.path.dirname(os.path.realpath(__file__))
ALAN_TOURING = json.load(open(os.path.join(pwd, "alan_turing.json")))
ALAN_TOURING_OLD = json.load(open(os.path.join(pwd, "alan_turing.old.json")))

revision_item_doc = revision.datasources.item_doc
parent_item_doc = revision.parent.datasources.item_doc
diff = revision.diff


def test_sitelinks_diff():
    cache = {revision_item_doc: ALAN_TOURING,
             parent_item_doc: ALAN_TOURING_OLD}

    sitelinks_diff = solve(diff.datasources.sitelinks_diff, cache=cache)
    eq_(sitelinks_diff.added,
        {'alswiki', 'fowiki', 'itwikiquote', 'commonswiki', 'mgwiki',
         'cywikiquote', 'ruwikiquote', 'kkwiki', 'ttwiki', 'cawikiquote',
         'eswikiquote', 'cewiki', 'cowiki', 'pawiki', 'cswikiquote',
         'hewikiquote', 'newwiki', 'uzwiki', 'zhwikiquote', 'bawiki',
         'furwiki', 'scowiki', 'dewikiquote', 'frwikiquote', 'plwikiquote',
         'enwikiquote'})
    eq_(sitelinks_diff.removed, set())
    eq_(sitelinks_diff.intersection,
        {'htwiki', 'mtwiki', 'swwiki', 'mkwiki', 'warwiki', 'anwiki', 'rowiki',
         'bgwiki', 'bnwiki', 'orwiki', 'idwiki', 'arwiki', 'skwiki', 'ruewiki',
         'tawiki', 'nnwiki', 'pnbwiki', 'guwiki', 'dewiki', 'cswiki',
         'ilowiki', 'kawiki', 'lvwiki', 'afwiki', 'jvwiki', 'zh_yuewiki',
         'tgwiki', 'hrwiki', 'brwiki', 'iswiki', 'ruwiki', 'dawiki', 'eswiki',
         'ltwiki', 'fawiki', 'bewiki', 'glwiki', 'iowiki', 'vowiki', 'yiwiki',
         'yowiki', 'plwiki', 'be_x_oldwiki', 'mlwiki', 'mswiki', 'astwiki',
         'hifwiki', 'urwiki', 'hewiki', 'aswiki', 'ocwiki', 'sawiki', 'cawiki',
         'tewiki', 'hiwiki', 'shwiki', 'pmswiki', 'trwiki', 'zh_min_nanwiki',
         'tlwiki', 'knwiki', 'jawiki', 'arzwiki', 'cywiki', 'lijwiki',
         'ptwiki', 'zhwiki', 'viwiki', 'mwlwiki', 'nlwiki', 'kowiki',
         'ganwiki', 'lawiki', 'simplewiki', 'bswiki', 'etwiki', 'slwiki',
         'huwiki', 'hywiki', 'sqwiki', 'srwiki', 'liwiki', 'lbwiki', 'fywiki',
         'mnwiki', 'fiwiki', 'lmowiki', 'jbowiki', 'thwiki', 'sahwiki',
         'euwiki', 'gawiki', 'azwiki', 'elwiki', 'kuwiki', 'ukwiki',
         'bat_smgwiki', 'pamwiki', 'mrwiki', 'enwiki', 'ckbwiki', 'frwiki',
         'eowiki', 'svwiki', 'gdwiki', 'scnwiki', 'itwiki', 'nowiki'})
    eq_(sitelinks_diff.changed, {'skwiki', 'sahwiki'})
    eq_(sitelinks_diff.unchanged,
        {'warwiki', 'aswiki', 'cywiki', 'lvwiki', 'sawiki', 'zh_yuewiki',
         'tewiki', 'pnbwiki', 'idwiki', 'mlwiki', 'anwiki', 'pmswiki',
         'kawiki', 'ptwiki', 'iowiki', 'ltwiki', 'bat_smgwiki', 'cswiki',
         'swwiki', 'rowiki', 'mswiki', 'etwiki', 'jvwiki', 'dawiki',
         'hifwiki', 'euwiki', 'simplewiki', 'htwiki', 'srwiki', 'huwiki',
         'bswiki', 'ilowiki', 'brwiki', 'hrwiki', 'eswiki', 'yiwiki', 'bnwiki',
         'glwiki', 'zhwiki', 'hiwiki', 'tawiki', 'eowiki', 'kowiki', 'yowiki',
         'jawiki', 'scnwiki', 'slwiki', 'astwiki', 'lijwiki', 'nnwiki',
         'svwiki', 'ruwiki', 'tlwiki', 'bgwiki', 'pamwiki', 'sqwiki', 'tgwiki',
         'gdwiki', 'fiwiki', 'mwlwiki', 'mnwiki', 'lmowiki', 'ukwiki',
         'arwiki', 'hewiki', 'enwiki', 'orwiki', 'lbwiki', 'thwiki', 'fywiki',
         'knwiki', 'elwiki', 'frwiki', 'shwiki', 'itwiki', 'azwiki',
         'zh_min_nanwiki', 'gawiki', 'liwiki', 'iswiki', 'trwiki', 'cawiki',
         'nlwiki', 'be_x_oldwiki', 'kuwiki', 'lawiki', 'bewiki', 'guwiki',
         'urwiki', 'nowiki', 'fawiki', 'jbowiki', 'ruewiki', 'afwiki',
         'arzwiki', 'ganwiki', 'ckbwiki', 'ocwiki', 'plwiki', 'dewiki',
         'viwiki', 'hywiki', 'mkwiki', 'mrwiki', 'mtwiki', 'vowiki'})

    eq_(pickle.loads(pickle.dumps(diff.datasources.sitelinks_diff)),
        diff.datasources.sitelinks_diff)


def test_labels_diff():
    cache = {revision_item_doc: ALAN_TOURING,
             parent_item_doc: ALAN_TOURING_OLD}

    labels_diff = solve(diff.datasources.labels_diff, cache=cache)
    eq_(labels_diff.added,
        {'tt', 'fo', 'pa', 'nan', 'sgs', 'mg', 'zh-cn', 'ba', 'fur', 'sco',
         'co', 'gsw', 'uz', 'kk', 'zh-hans', 'new', 'ce', 'de-ch'})
    eq_(labels_diff.removed,
        {'simple', 'zh-yue', 'bat-smg', 'be-x-old', 'zh-min-nan', 'no'})
    eq_(labels_diff.intersection,
        {'jv', 'gl', 'te', 'war', 'pt', 'de', 'gd', 'sq', 'lv', 'hif', 'hy',
         'hr', 'rue', 'pnb', 'ca', 'ka', 'nl', 'sr', 'gan', 'ur', 'vi', 'bg',
         'scn', 'th', 'ast', 'az', 'tl', 'mr', 'af', 'zh', 'ko', 'be', 'ja',
         'ml', 'ilo', 'oc', 'cs', 'lb', 'yue', 'fi', 'sw', 'pl', 'es', 'eo',
         'arz', 'nb', 'nn', 'ru', 'tr', 'mk', 'sa', 'en-gb', 'mn', 'br',
         'sah', 'ro', 'yo', 'is', 'el', 'jbo', 'he', 'en', 'hi', 'bs', 'id',
         'gu', 'sv', 'lmo', 'pt-br', 'an', 'kn', 'ar', 'it', 'mt', 'tg', 'io',
         'ms', 'sh', 'eu', 'or', 'li', 'pam', 'pms', 'la', 'mwl', 'lij', 'da',
         'vo', 'fr', 'uk', 'fy', 'lt', 'bn', 'et', 'ku', 'ht', 'yi', 'ckb',
         'sk', 'fa', 'hu', 'as', 'be-tarask', 'ta', 'ga', 'sl', 'cy', 'en-ca'})
    eq_(labels_diff.changed, {'ru', 'eo'})
    eq_(labels_diff.unchanged,
        {'ml', 'nn', 'hif', 'hr', 'hu', 'ar', 'ka', 'ko', 'vi', 'he', 'jbo',
         'sah', 'as', 'bs', 'ht', 'pam', 'scn', 'tr', 'tg', 'mr', 'mwl', 'nl',
         'io', 'rue', 'es', 'el', 'pnb', 'sq', 'nb', 'sk', 'ja', 'mt', 'de',
         'arz', 'it', 'sw', 'kn', 'ku', 'sa', 'or', 'sr', 'pt', 'zh', 'af',
         'cy', 'th', 'pt-br', 'hi', 'pms', 'jv', 'ta', 'fa', 'sl', 'fr', 'yo',
         'lij', 'li', 'en-gb', 'sv', 'hy', 'bg', 'lb', 'en', 'fi', 'lmo',
         'az', 'da', 'te', 'eu', 'ast', 'ms', 'gan', 'ca', 'la', 'ro', 'uk',
         'mn', 'mk', 'lt', 'vo', 'is', 'et', 'br', 'fy', 'yue', 'be', 'yi',
         'ga', 'bn', 'sh', 'gl', 'cs', 'ckb', 'ur', 'tl', 'pl', 'lv', 'id',
         'gd', 'war', 'gu', 'an', 'oc', 'en-ca', 'be-tarask', 'ilo'})

    eq_(pickle.loads(pickle.dumps(diff.datasources.labels_diff)),
        diff.datasources.labels_diff)


def test_aliases_diff():
    cache = {revision_item_doc: ALAN_TOURING,
             parent_item_doc: ALAN_TOURING_OLD}

    aliases_diff = solve(diff.datasources.aliases_diff, cache=cache)
    eq_(aliases_diff.added,
        {'ko', 'ru'})
    eq_(aliases_diff.removed, set())
    eq_(aliases_diff.intersection,
        {'ja', 'fr', 'de', 'be-tarask', 'jbo', 'en', 'it'})
    eq_(aliases_diff.changed, set())
    eq_(aliases_diff.unchanged,
        {'en', 'be-tarask', 'de', 'jbo', 'it', 'fr', 'ja'})

    eq_(pickle.loads(pickle.dumps(diff.datasources.aliases_diff)),
        diff.datasources.aliases_diff)


def test_descriptions_diff():
    cache = {revision_item_doc: ALAN_TOURING,
             parent_item_doc: ALAN_TOURING_OLD}

    descriptions_diff = solve(diff.datasources.descriptions_diff, cache=cache)
    eq_(descriptions_diff.added,
        {'da', 'sk', 'as', 'zh-cn', 'pl', 'ru', 'nl', 'zh', 'gl', 'nn', 'pam',
         'nb', 'sv', 'ko', 'zh-hans'})
    eq_(descriptions_diff.removed, set())
    eq_(descriptions_diff.intersection,
        {'en', 'it', 'fr', 'es', 'ilo', 'fa', 'de'})
    eq_(descriptions_diff.changed, {'fa'})
    eq_(descriptions_diff.unchanged, {'fr', 'it', 'es', 'de', 'en', 'ilo'})

    eq_(pickle.loads(pickle.dumps(diff.datasources.descriptions_diff)),
        diff.datasources.descriptions_diff)


def test_properties_diff():
    cache = {revision_item_doc: ALAN_TOURING,
             parent_item_doc: ALAN_TOURING_OLD}

    properties_diff = solve(diff.datasources.properties_diff, cache=cache)
    eq_(properties_diff.added,
        {'P31', 'P1741', 'P950', 'P935', 'P27', 'P1296', 'P1415', 'P1207',
         'P549', 'P512', 'P1343', 'P906', 'P1816', 'P735', 'P25', 'P1417',
         'P1412', 'P691', 'P949', 'P800', 'P1273', 'P1196', 'P1819', 'P646',
         'P140', 'P1563', 'P1430', 'P345', 'P1263', 'P1006', 'P166', 'P2021',
         'P910', 'P108', 'P22'})
    eq_(properties_diff.removed, {'P509', 'P107'})
    eq_(properties_diff.intersection,
        {'P69', 'P268', 'P213', 'P106', 'P20', 'P19', 'P214', 'P269', 'P91',
         'P570', 'P18', 'P185', 'P227', 'P101', 'P463', 'P535', 'P373', 'P184',
         'P244', 'P21', 'P349', 'P569'})
    eq_(properties_diff.changed,
        {'P19', 'P570', 'P91', 'P569', 'P20', 'P227', 'P101', 'P69', 'P21',
         'P106'})
    eq_(properties_diff.unchanged,
        {'P244', 'P269', 'P268', 'P535', 'P18', 'P373', 'P185', 'P213', 'P463',
         'P349', 'P184', 'P214'})

    eq_(pickle.loads(pickle.dumps(diff.datasources.properties_diff)),
        diff.datasources.properties_diff)

    eq_(solve(diff.properties_added, cache=cache), 35)
    eq_(solve(diff.properties_removed, cache=cache), 2)
    eq_(solve(diff.properties_changed, cache=cache), 10)

    eq_(pickle.loads(pickle.dumps(diff.properties_added)),
        diff.properties_added)
    eq_(pickle.loads(pickle.dumps(diff.properties_removed)),
        diff.properties_removed)
    eq_(pickle.loads(pickle.dumps(diff.properties_changed)),
        diff.properties_changed)


def test_claims_diff():
    cache = {revision_item_doc: ALAN_TOURING,
             parent_item_doc: ALAN_TOURING_OLD}

    eq_({c.id for c in solve(diff.datasources.claims_added, cache=cache)},
        {'P1430', 'P1006', 'P691', 'P512', 'P1816', 'P735', 'P646', 'P1412',
         'P1196', 'P2021', 'P950', 'P1273', 'P31', 'P1563', 'P906', 'P949',
         'P106', 'P1417', 'P22', 'P1263', 'P549', 'P19', 'P1207', 'P1415',
         'P345', 'P1741', 'P800', 'P1296', 'P910', 'P166', 'P140', 'P108',
         'P1819', 'P935', 'P25', 'P69', 'P27', 'P1343'})
    eq_({c.id for c in solve(diff.datasources.claims_removed, cache=cache)},
        {'P107', 'P509'})
    eq_({c.id for c, _ in solve(diff.datasources.claims_changed, cache=cache)},
        {'P21', 'P570', 'P101', 'P19', 'P106', 'P91', 'P20', 'P69', 'P569',
         'P227'})

    eq_(solve(diff.claims_added, cache=cache), 46)
    eq_(solve(diff.claims_removed, cache=cache), 2)
    eq_(solve(diff.claims_changed, cache=cache), 10)

    eq_(pickle.loads(pickle.dumps(diff.claims_added)),
        diff.claims_added)
    eq_(pickle.loads(pickle.dumps(diff.claims_removed)),
        diff.claims_removed)
    eq_(pickle.loads(pickle.dumps(diff.claims_changed)),
        diff.claims_changed)


def test_sources_diff():
    cache = {revision_item_doc: ALAN_TOURING,
             parent_item_doc: ALAN_TOURING_OLD}

    eq_({c.id for c in solve(diff.datasources.sources_added, cache=cache)},
        {'P813', 'P248', 'P854', 'P143', 'P345'})
    eq_({c.id for c in solve(diff.datasources.sources_removed, cache=cache)},
        {'P143'})

    eq_(solve(diff.sources_added, cache=cache), 26)
    eq_(solve(diff.sources_removed, cache=cache), 1)
    eq_(pickle.loads(pickle.dumps(diff.sources_added)),
        diff.sources_added)
    eq_(pickle.loads(pickle.dumps(diff.sources_removed)),
        diff.sources_removed)


def test_qualifiers_diff():
    # TODO: Ladsgroup, this test seems wrong
    cache = {revision_item_doc: ALAN_TOURING,
             parent_item_doc: ALAN_TOURING_OLD}

    eq_({c.id for c in solve(diff.datasources.qualifiers_added, cache=cache)},
        set())
    eq_({c.id for c in solve(diff.datasources.qualifiers_removed,
                             cache=cache)},
        set())

    eq_(solve(diff.qualifiers_added, cache=cache), 0)
    eq_(solve(diff.qualifiers_removed, cache=cache), 0)

    eq_(pickle.loads(pickle.dumps(diff.qualifiers_added)),
        diff.qualifiers_added)
    eq_(pickle.loads(pickle.dumps(diff.qualifiers_removed)),
        diff.qualifiers_removed)


def test_badges_diff():
    cache = {revision_item_doc: ALAN_TOURING,
             parent_item_doc: ALAN_TOURING_OLD}

    badges_diff = solve(diff.datasources.badges_diff, cache=cache)
    eq_(badges_diff.added, {'lawiki', 'aswiki', 'enwiki', 'ruwiki', 'azwiki'})
    eq_(badges_diff.removed, set())
    eq_(badges_diff.intersection, set())
    eq_(badges_diff.changed, set())
    eq_(badges_diff.unchanged, set())

    eq_(pickle.loads(pickle.dumps(diff.datasources.badges_diff)),
        diff.datasources.badges_diff)

    eq_(solve(diff.badges_added, cache=cache), 5)
    eq_(solve(diff.badges_removed, cache=cache), 0)
    eq_(solve(diff.badges_changed, cache=cache), 0)

    eq_(pickle.loads(pickle.dumps(diff.badges_added)), diff.badges_added)
    eq_(pickle.loads(pickle.dumps(diff.badges_removed)), diff.badges_removed)
    eq_(pickle.loads(pickle.dumps(diff.badges_changed)), diff.badges_changed)


def test_proportion_of_qid_added():
    cache = {revision_item_doc: ALAN_TOURING,
             parent_item_doc: ALAN_TOURING_OLD}

    eq_(round(solve(diff.proportion_of_qid_added, cache=cache), 2), 0.95)
    eq_(pickle.loads(pickle.dumps(diff.proportion_of_qid_added)),
        diff.proportion_of_qid_added)


def test_proportion_of_language_added():
    cache = {revision_item_doc: ALAN_TOURING,
             parent_item_doc: ALAN_TOURING_OLD}

    eq_(round(solve(diff.proportion_of_language_added, cache=cache), 2), 0.0)
    eq_(pickle.loads(pickle.dumps(diff.proportion_of_language_added)),
        diff.proportion_of_language_added)


def test_proportion_of_links_added():
    cache = {revision_item_doc: ALAN_TOURING,
             parent_item_doc: ALAN_TOURING_OLD}

    eq_(round(solve(diff.proportion_of_links_added, cache=cache), 2), 0.87)
    eq_(pickle.loads(pickle.dumps(diff.proportion_of_links_added)),
        diff.proportion_of_links_added)


def test_identifiers_changed():
    cache = {revision_item_doc: ALAN_TOURING,
             parent_item_doc: ALAN_TOURING_OLD}

    eq_(round(solve(diff.identifiers_changed, cache=cache), 2), 1)
    eq_(pickle.loads(pickle.dumps(diff.identifiers_changed)),
        diff.identifiers_changed)


def test_property_changed():
    p999_changed = diff.property_changed('P999')
    p19_changed = diff.property_changed('P19')

    cache = {revision_item_doc: ALAN_TOURING,
             parent_item_doc: ALAN_TOURING_OLD}

    eq_(solve(p999_changed, cache=cache), False)
    eq_(solve(p19_changed, cache=cache), True)

    eq_(pickle.loads(pickle.dumps(p999_changed)), p999_changed)
    eq_(pickle.loads(pickle.dumps(p19_changed)), p19_changed)
