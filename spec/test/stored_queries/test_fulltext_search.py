"""
Tests for the generic fulltext search

These tests run within the re_api docker image, and require access to the ArangoDB, auth, and workspace images.
"""
import json
import time
import unittest
import requests
import os

from spec.test.helpers import (
    get_config,
    check_spec_test_env,
    create_test_docs,
)

_CONF = get_config()
_NOW = int(time.time() * 1000)
LIMIT = 20  # default

TEST_DATA_DIR = os.path.normpath(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '../data/'
    )
)

ncbi_taxon_fp = os.path.join(TEST_DATA_DIR, 'ncbi_taxon.json')
with open(ncbi_taxon_fp) as fh:
    ncbi_taxa = json.load(fh)

gtdb_taxon_fp = os.path.join(TEST_DATA_DIR, 'gtdb_taxon.json')
with open(gtdb_taxon_fp) as fh:
    gtdb_taxa = json.load(fh)

silva_taxon_fp = os.path.join(TEST_DATA_DIR, 'silva_taxon.json')
with open(silva_taxon_fp) as fh:
    silva_taxa = json.load(fh)


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('\n###SPEC_RELEASE_PATH', os.environ.get('SPEC_RELEASE_PATH'))
        check_spec_test_env(do_download_specs=True)

        create_test_docs('ncbi_taxon', ncbi_taxa)
        create_test_docs('gtdb_taxon', gtdb_taxa)
        create_test_docs('silva_taxon', silva_taxa)

        print('DONE. AND SPEC_RELEASE_PATH IS', os.environ.get('SPEC_RELEASE_PATH'))

    def test_ncbi_taxon_scinames(self):
        scinames = [
            # --- Token preceded by punctuation ---
            "Lactobacillus sp. 'thermophilus'",
            "Rabbit fibroma virus (strain Kasza)",
            "'Prunus' dulcis",
            # --- Tokens joined by punctuation
            'Lactococcus phage 936 group phage Phi13.16',
            'Pseudogobio cf. esocinus CBM:ZF:12684',
            'Klebsormidium sp. BIOTA 14615.5a',
            # --- Misc gnarly ---
            'Influenza C virus (C/PIG/Beijing/439/1982)',
            'Bovine herpesvirus type 1.1 (strain P8-2)',
            'Porcine transmissible gastroenteritis coronavirus strain FS772/70',
            'Salmonella enterica subsp. houtenae serovar 16:z4,z32:--',
            'Influenza A virus PX8-XIII(A/USSR/90/77(H1N1)xA/Pintail Duck/Primorie/695/76(H2N3))',
            'Influenza B virus (B/Ann Arbor/1/1966 [cold-adapted and wild- type])',
            # --- Prefix 1 ---
            'Vaccinia virus WR 65-16',
            'Dengue virus 2 Jamaica/1409/1983',
            'Dengue virus 2 Thailand/NGS-C/1944',
            # --- Dups ---
            'environmental samples',
            'Listeria sp. FSL_L7-0091',
            'Listeria sp. FSL_L7-1519',
            # --- Misc ---
            'Norovirus GII.9',
            'Corticiaceae sp.',
            'Escherichia coli',
        ]
        for sciname in scinames:
            _fulltext_query__expect_hit(
                self,
                coll='ncbi_taxon',
                search_attrkey='scientific_name',
                search_text=sciname,
                ts=_NOW,
                filter_attr_expr=[{'rank': 'species'}, {'rank': 'strain'}, {'strain': True}],
                offset=None,
                limit=LIMIT,
                select=['scientific_name']
            )

    def test_gtdb_taxon_scinames(self):
        scinames = [
            'Breoghania corrubedonensis',
            'Streptomyces alfalfae',
            'Streptococcus parasanguinis_C',
            'Bacillus_H clausii_B',
            'Acidibacillus ferrooxidans_B',
            'Streptomyces prasinopilosus',
            'Mesorhizobium kowhaii',
            'UBA10025 sp001003705',
            'PEYC01 sp002774555',
            'Pelagibacter sp003213695',
            'Planktomarina sp000981705',
            'Pelagibacter sp003216255',
            'Pseudopedobacter glucosidilyticus_B',
            'Micromonospora chokoriensis_B',
            'Ardenticatena maritima',
            'ZC4RG35 sp003242515',
            'UBA3792 sp900318765',
            'Rugosibacter sp002842395',
            'Nitratiruptor sp000010325',
            'GWF2-35-18 sp001771135',
            'Prevotella histicola',
            'Prevotella stercorea',
            'GCA-2722175 sp002722175',
            'Maribacter thermophilus',
            'Cyanothece sp000022045',
            'Vibrio aphrogenes',
            'Actinoplanes missouriensis',
            'S36-B12 sp002729215',
            'Accumulibacter sp000585015',
            'Raineya orbicola',
            'Prochlorococcus_A sp003281125',
            'Bifidobacterium catenulatum',
            'UBA4466 sp002709305',
            'Aurantimonas coralicida',
            'Marinomonas arctica'
        ]

        for sciname in scinames:
            _fulltext_query__expect_hit(
                self,
                coll='gtdb_taxon',
                search_attrkey='name',
                search_text=sciname,
                ts=_NOW,
                filter_attr_expr=[{'rank': 'species'}],
                offset=None,
                limit=LIMIT,
                select=['name'],
            )

    def test_silva_taxon_scinames(self):
        # These are all high q seqs
        scinames = [
            'uncultured bacterium',
            'Microbacterium sp. RB-01',
            'Lactobacillus sakei subsp. carnosus',
            'Lactobacillus sp.',
            'Desulfovibrio biadhensis',
            'Candidatus Hodgkinia cicadicola',
            'Durinskia baltica',
            'gamma proteobacterium symbiont of Hermolaus amurensis',
            'Kakapolichus sp. n. AD881',
            'Pseudanabaena sp. MBIC10772',
            'Pantoea agglomerans',
            'Pantoea stewartii subsp. indologenes',
            'Fictibacillus barbaricus',
            'Aeromonas veronii',
            'Shigella sp. JN-4',
            'Streptomyces virginiae',
            'Serratia grimesii',
            'Streptococcus pneumoniae OXC141',
            'Sphingobacterium sp.',
            'Meliboeithon intermedium',
            'Rhodococcus coprophilus',
            'Nysius sp. HL-2004',
            'Pseudoalteromonas sp. SBN2-2',
            'Xanthomonadaceae bacterium AF4',
            'Geobacillus thermodenitrificans',
            'Perinereis sp. PR-2017',
            'unidentified',
            'Vibrio alginolyticus',
            'uncultured actinobacterium',
            'Streptomyces sp. INBio_4516X',
            'uncultured Petrimonas sp.',
            'Corynebacterium xerosis',
            'Phyllium bioculatum',
            'Pseudomonas stutzeri',
            'Streptococcus pyogenes'
        ]

        for sciname in scinames:
            _fulltext_query__expect_hit(
                self,
                coll='silva_taxon',
                search_attrkey='name',
                search_text=sciname,
                ts=_NOW,
                filter_attr_expr=[
                    {
                        'rank': 'sequence',
                        'datasets': ['parc', 'ref', 'nr99'],  # high q seqs
                    }, {
                        'rank': 'sequence',
                        'datasets': ['parc', 'ref'],  # med q seqs
                    }
                ],
                offset=None,
                limit=LIMIT,
                select=['name'],
            )

    def test_unspecified_bind_params(self):
        scinames = [
            'Escherichia coli',
        ]
        for sciname in scinames:
            _fulltext_query__expect_hit(
                self,
                coll='ncbi_taxon',
                search_attrkey='scientific_name',
                search_text=sciname,
                ts=None,
                filter_attr_expr=None,
                offset=None,
                limit=None,
                select=None,
            )

    def test_specified_bind_parameters(self):
        scinames = [
            'Escherichia coli',
        ]
        for sciname in scinames:
            _fulltext_query__expect_hit(
                self,
                coll='ncbi_taxon',
                search_attrkey='scientific_name',
                search_text=sciname,
                ts=_NOW,
                filter_attr_expr=[{'rank': 'species'}, {'rank': 'strain'}, {'strain': True}],
                offset=0,
                limit=LIMIT,
                select=['scientific_name']
            )


# --- Test helpers ---


def _fulltext_query__expect_hit(
    self,
    coll,
    search_attrkey,
    search_text,
    ts,
    filter_attr_expr,
    offset,
    limit,
    select,
):
    """
    Helper to run the taxonomy_search_sci_name query and make some standard
    assertions on the response.
    """
    data = {
        '@coll': coll,
        'search_attrkey': search_attrkey,
        'search_text': search_text,
        'ts': ts,
        'filter_attr_expr': filter_attr_expr,
        'offset': offset,
        'limit': limit,
        'select': select,
    }
    resp = requests.post(
        _CONF["re_api_url"] + "/api/v1/query_results",
        params={"stored_query": "fulltext_search"},
        data=json.dumps(data),
    ).json()
    print('######################################################################')
    print(json.dumps(resp, indent=4).replace(r'\n', '\n'))
    print('######################################################################')

    results = resp['results'][0]
    docs = results['result']
    hits = [doc[search_attrkey] for doc in docs]
    self.assertIn(search_text, hits)
    self.assertFalse(len(hits) == limit and len(set(hits) == 1))  # check not just overflowing with dups
