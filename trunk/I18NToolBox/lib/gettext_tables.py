# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: gettext_tables.py 8 2006-12-27 20:58:31Z s0undt3ch $
# =============================================================================
# $URL: http://i18ntoolbox.ufsoft.org/svn/trunk/I18NToolBox/lib/gettext_tables.py $
# $LastChangedDate: 2006-12-27 20:58:31 +0000 (Wed, 27 Dec 2006) $
# $Rev: 8 $
# $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

plurals_table = (
    ( "hu", "Hungarian",         "1", "0" ),
    ( "ja", "Japanese",          "1", "0" ),
    ( "ko", "Korean",            "1", "0" ),
    ( "tr", "Turkish",           "1", "0" ),
    ( "da", "Danish",            "2", "(n != 1)" ),
    ( "nl", "Dutch",             "2", "(n != 1)" ),
    ( "en", "English",           "2", "(n != 1)" ),
    ( "de", "German",            "2", "(n != 1)" ),
    ( "nb", "Norwegian Bokmal",  "2", "(n != 1)" ),
    ( "no", "Norwegian",         "2", "(n != 1)" ),
    ( "nn", "Norwegian Nynorsk", "2", "(n != 1)" ),
    ( "sv", "Swedish",           "2", "(n != 1)" ),
    ( "et", "Estonian",          "2", "(n != 1)" ),
    ( "fi", "Finnish",           "2", "(n != 1)" ),
    ( "el", "Greek",             "2", "(n != 1)" ),
    ( "he", "Hebrew",            "2", "(n != 1)" ),
    ( "it", "Italian",           "2", "(n != 1)" ),
    ( "pt", "Portuguese",        "2", "(n != 1)" ),
    ( "es", "Spanish",           "2", "(n != 1)" ),
    ( "eo", "Esperanto",         "2", "(n != 1)" ),
    ( "fr", "French",            "2", "(n > 1)" ),
    ( "pt_BR", "Brazilian",      "2", "(n > 1)" ),
    ( "lv", "Latvian",           "3", "(n%10==1 && n%100!=11 ? 0 : n != 0 ? 1 : 2)" ),
    ( "ga", "Irish",             "3", "n==1 ? 0 : n==2 ? 1 : 2" ),
    ( "lt", "Lithuanian",        "3", "(n%10==1 && n%100!=11 ? 0 : n%10>=2 && (n%100<10 || n%100>=20) ? 1 : 2)" ),
    ( "hr", "Croatian",          "3", "(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2)" ),
    ( "cs", "Czech",             "3", "(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2)" ),
    ( "ru", "Russian",           "3", "(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2)" ),
    ( "sk", "Slovak",            "3", "(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2)" ),
    ( "uk", "Ukrainian",         "3", "(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2)" ),
    ( "pl", "Polish",            "3", "(n==1 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2)" ),
    ( "sl", "Slovenian",         "4", "(n%100==1 ? 0 : n%100==2 ? 1 : n%100==3 || n%100==4 ? 2 : 3)" )
)

lang_table = (
    ( "aa",     "Afar" ),
    ( "ab",     "Abkhazian" ),
    ( "ace",    "Achinese" ),
    ( "ad",     "Adangme" ),
    ( "ae",     "Avestan" ),
    ( "af",     "Afrikaans" ),
    ( "ak",     "Akan" ),
    ( "am",     "Amharic" ),
    ( "an",     "Aragonese" ),
    ( "ang",    "Old English" ),
    ( "ar",     "Arabic" ),
    ( "as",     "Assamese" ),
    ( "av",     "Avaric" ),
    ( "awa",    "Awadhi" ),
    ( "ay",     "Aymara" ),
    ( "az",     "Azerbaijani" ),
    ( "ba",     "Bashkir" ),
    ( "bad",    "Banda" ),
    ( "bal",    "Baluchi" ),
    ( "ban",    "Balinese" ),
    ( "be",     "Belarusian" ),
    ( "bem",    "Bemba" ),
    ( "bg",     "Bulgarian" ),
    ( "bh",     "Bihari" ),
    ( "bho",    "Bhojpuri" ),
    ( "bi",     "Bislama" ),
    ( "bik",    "Bikol" ),
    ( "bin",    "Bini" ),
    ( "bm",     "Bambara" ),
    ( "bn",     "Bengali" ),
    ( "bo",     "Tibetan" ),
    ( "br",     "Breton" ),
    ( "bs",     "Bosnian" ),
    ( "btk",    "Batak" ),
    ( "bug",    "Buginese" ),
    ( "ca",     "Catalan" ),
    ( "ce",     "Chechen" ),
    ( "ceb",    "Cebuano" ),
    ( "ch",     "Chamorro" ),
    ( "co",     "Corsican" ),
    ( "cr",     "Cree" ),
    ( "cs",     "Czech" ),
    ( "csb",    "Kashubian" ),
    ( "cu",     "Church Slavic" ),
    ( "cv",     "Chuvash" ),
    ( "cy",     "Welsh" ),
    ( "da",     "Danish" ),
    ( "de",     "German" ),
    ( "din",    "Dinka" ),
    ( "doi",    "Dogri" ),
    ( "dv",     "Divehi" ),
    ( "dz",     "Dzongkha" ),
    ( "ee",     "Ewe" ),
    ( "el",     "Greek" ),
    ( "en",     "English" ),
    ( "eo",     "Esperanto" ),
    ( "es",     "Spanish" ),
    ( "et",     "Estonian" ),
    ( "eu",     "Basque" ),
    ( "fa",     "Persian" ),
    ( "ff",     "Fulah" ),
    ( "fi",     "Finnish" ),
    ( "fil",    "Filipino" ),
    ( "fj",     "Fijian" ),
    ( "fo",     "Faroese" ),
    ( "fon",    "Fon" ),
    ( "fr",     "French" ),
    ( "fy",     "Western Frisian" ),
    ( "ga",     "Irish" ),
    ( "gd",     "Scots" ),
    ( "gl",     "Galician" ),
    ( "gn",     "Guarani" ),
    ( "gon",    "Gondi" ),
    ( "gsw",    "Swiss German" ),
    ( "gu",     "Gujarati" ),
    ( "gv",     "Manx" ),
    ( "ha",     "Hausa" ),
    ( "he",     "Hebrew" ),
    ( "hi",     "Hindi" ),
    ( "hil",    "Hiligaynon" ),
    ( "hmn",    "Hmong" ),
    ( "ho",     "Hiri Motu" ),
    ( "hr",     "Croatian" ),
    ( "ht",     "Haitian" ),
    ( "hu",     "Hungarian" ),
    ( "hy",     "Armenian" ),
    ( "hz",     "Herero" ),
    ( "ia",     "Interlingua" ),
    ( "id",     "Indonesian" ),
    ( "ie",     "Interlingue" ),
    ( "ig",     "Igbo" ),
    ( "ii",     "Sichuan Yi" ),
    ( "ik",     "Inupiak" ),
    ( "ilo",    "Iloko" ),
    ( "is",     "Icelandic" ),
    ( "it",     "Italian" ),
    ( "iu",     "Inuktitut" ),
    ( "ja",     "Japanese" ),
    ( "jab",    "Hyam" ),
    ( "jw",     "Javanese" ),
    ( "ka",     "Georgian" ),
    ( "kab",    "Kabyle" ),
    ( "kaj",    "Jju" ),
    ( "kam",    "Kamba" ),
    ( "kbd",    "Kabardian" ),
    ( "kcg",    "Tyap" ),
    ( "kdm",    "Kagoma" ),
    ( "kg",     "Kongo" ),
    ( "ki",     "Kikuyu" ),
    ( "kj",     "Kuanyama" ),
    ( "kk",     "Kazakh" ),
    ( "kl",     "Kalaallisut" ),
    ( "km",     "Khmer" ),
    ( "kmb",    "Kimbundu" ),
    ( "kn",     "Kannada" ),
    ( "ko",     "Korean" ),
    ( "kr",     "Kanuri" ),
    ( "kru",    "Kurukh" ),
    ( "ks",     "Kashmiri" ),
    ( "ku",     "Kurdish" ),
    ( "kv",     "Komi" ),
    ( "kw",     "Cornish" ),
    ( "ky",     "Kirghiz" ),
    ( "kok",    "Konkani" ),
    ( "la",     "Latin" ),
    ( "lb",     "Letzeburgesch" ),
    ( "lg",     "Ganda" ),
    ( "li",     "Limburgish" ),
    ( "ln",     "Lingala" ),
    ( "lo",     "Laotian" ),
    ( "lt",     "Lithuanian" ),
    ( "lu",     "Luba-Katanga" ),
    ( "lua",    "Luba-Lulua" ),
    ( "luo",    "Luo" ),
    ( "lv",     "Latvian" ),
    ( "mad",    "Madurese" ),
    ( "mag",    "Magahi" ),
    ( "mai",    "Maithili" ),
    ( "mak",    "Makasar" ),
    ( "man",    "Mandingo" ),
    ( "men",    "Mende" ),
    ( "mg",     "Malagasy" ),
    ( "mh",     "Marshallese" ),
    ( "mi",     "Maori" ),
    ( "min",    "Minangkabau" ),
    ( "mk",     "Macedonian" ),
    ( "ml",     "Malayalam" ),
    ( "mn",     "Mongolian" ),
    ( "mni",    "Manipuri" ),
    ( "mo",     "Moldavian" ),
    ( "mos",    "Mossi" ),
    ( "mr",     "Marathi" ),
    ( "ms",     "Malay" ),
    ( "mt",     "Maltese" ),
    ( "mwr",    "Marwari" ),
    ( "my",     "Burmese" ),
    ( "myn",    "Mayan" ),
    ( "na",     "Nauru" ),
    ( "nap",    "Neapolitan" ),
    ( "nah",    "Nahuatl" ),
    ( "nb",     "Norwegian Bokmal" ),
    ( "nd",     "North Ndebele" ),
    ( "nds",    "Low Saxon" ),
    ( "ne",     "Nepali" ),
    ( "ng",     "Ndonga" ),
    ( "nl",     "Dutch" ),
    ( "nn",     "Norwegian Nynorsk" ),
    ( "no",     "Norwegian" ),
    ( "nr",     "South Ndebele" ),
    ( "nso",    "Northern Sotho" ),
    ( "nv",     "Navajo" ),
    ( "ny",     "Nyanja" ),
    ( "nym",    "Nyamwezi" ),
    ( "nyn",    "Nyankole" ),
    ( "oc",     "Occitan" ),
    ( "oj",     "Ojibwa" ),
    ( "om",     "(Afan) Oromo" ),
    ( "or",     "Oriya" ),
    ( "os",     "Ossetian" ),
    ( "pa",     "Punjabi" ),
    ( "pag",    "Pangasinan" ),
    ( "pam",    "Pampanga" ),
    ( "pbb",    "Páez" ),
    ( "pi",     "Pali" ),
    ( "pl",     "Polish" ),
    ( "ps",     "Pashto" ),
    ( "pt",     "Portuguese" ),
    ( "qu",     "Quechua" ),
    ( "raj",    "Rajasthani" ),
    ( "rm",     "Rhaeto-Roman" ),
    ( "rn",     "Kirundi" ),
    ( "ro",     "Romanian" ),
    ( "ru",     "Russian" ),
    ( "rw",     "Kinyarwanda" ),
    ( "sa",     "Sanskrit" ),
    ( "sas",    "Sasak" ),
    ( "sat",    "Santali" ),
    ( "sc",     "Sardinian" ),
    ( "scn",    "Sicilian" ),
    ( "sd",     "Sindhi" ),
    ( "se",     "Northern Sami" ),
    ( "sg",     "Sango" ),
    ( "shn",    "Shan" ),
    ( "si",     "Sinhala" ),
    ( "sid",    "Sidamo" ),
    ( "sk",     "Slovak" ),
    ( "sl",     "Slovenian" ),
    ( "sm",     "Samoan" ),
    ( "sn",     "Shona" ),
    ( "so",     "Somali" ),
    ( "sq",     "Albanian" ),
    ( "sr",     "Serbian" ),
    ( "srr",    "Serer" ),
    ( "ss",     "Siswati" ),
    ( "st",     "Sesotho" ),
    ( "su",     "Sundanese" ),
    ( "suk",    "Sukuma" ),
    ( "sus",    "Susu" ),
    ( "sv",     "Swedish" ),
    ( "sw",     "Swahili" ),
    ( "ta",     "Tamil" ),
    ( "te",     "Telugu" ),
    ( "tem",    "Timne" ),
    ( "tet",    "Tetum" ),
    ( "tg",     "Tajik" ),
    ( "th",     "Thai" ),
    ( "ti",     "Tigrinya" ),
    ( "tiv",    "Tiv" ),
    ( "tk",     "Turkmen" ),
    ( "tl",     "Tagalog" ),
    ( "tn",     "Setswana" ),
    ( "to",     "Tonga" ),
    ( "tr",     "Turkish" ),
    ( "ts",     "Tsonga" ),
    ( "tt",     "Tatar" ),
    ( "tum",    "Tumbuka" ),
    ( "tw",     "Twi" ),
    ( "ty",     "Tahitian" ),
    ( "ug",     "Uighur" ),
    ( "uk",     "Ukrainian" ),
    ( "umb",    "Umbundu" ),
    ( "ur",     "Urdu" ),
    ( "uz",     "Uzbek" ),
    ( "ve",     "Venda" ),
    ( "vi",     "Vietnamese" ),
    ( "vo",     "Volapuk" ),
    ( "wal",    "Walamo" ),
    ( "war",    "Waray" ),
    ( "wen",    "Sorbian" ),
    ( "wo",     "Wolof" ),
    ( "xh",     "Xhosa" ),
    ( "yao",    "Yao" ),
    ( "yi",     "Yiddish" ),
    ( "yo",     "Yoruba" ),
    ( "za",     "Zhuang" ),
    ( "zh",     "Chinese" ),
    ( "zu",     "Zulu" ),
    ( "zap",    "Zapotec" )
)

locales_table = (
                # Language              Main territory
                # ------------------------------------------------
    "ace_ID",   # Achinese              Indonesia 
    "af_ZA",    # Afrikaans             South Africa 
    "ak_GH",    # Akan                  Ghana 
    "am_ET",    # Amharic               Ethiopia 
    "an_ES",    # Aragonese             Spain 
    "ang_GB",   # Old English           Britain 
    "as_IN",    # Assamese              India 
    "av_RU",    # Avaric                Russia 
    "awa_IN",   # Awadhi                India 
    "az_AZ",    # Azerbaijani           Azerbaijan 
    "bad_CF",   # Banda                 Central African Republic 
    "ban_ID",   # Balinese              Indonesia 
    "be_BY",    # Belarusian            Belarus 
    "bem_ZM",   # Bemba                 Zambia 
    "bg_BG",    # Bulgarian             Bulgaria 
    "bho_IN",   # Bhojpuri              India 
    "bik_PH",   # Bikol                 Philippines 
    "bin_NG",   # Bini                  Nigeria 
    "bm_ML",    # Bambara               Mali 
    "bn_IN",    # Bengali               India 
    "bo_CN",    # Tibetan               China 
    "br_FR",    # Breton                France 
    "bs_BA",    # Bosnian               Bosnia 
    "btk_ID",   # Batak                 Indonesia 
    "bug_ID",   # Buginese              Indonesia 
    "ca_ES",    # Catalan               Spain 
    "ce_RU",    # Chechen               Russia 
    "ceb_PH",   # Cebuano               Philippines 
    "co_FR",    # Corsican              France 
    "cr_CA",    # Cree                  Canada 
    "cs_CZ",    # Czech                 Czech Republic 
    "csb_PL",   # Kashubian             Poland 
    "cy_GB",    # Welsh                 Britain 
    "da_DK",    # Danish                Denmark 
    "de_DE",    # German                Germany 
    "din_SD",   # Dinka                 Sudan 
    "doi_IN",   # Dogri                 India 
    "dv_MV",    # Divehi                Maldives 
    "dz_BT",    # Dzongkha              Bhutan 
    "ee_GH",    # Éwé                   Ghana 
    "el_GR",    # Greek                 Greece 
    # Don't put "en_GB" or "en_US" here.  That would be asking for fruitless
    #   political discussion.  
    "es_ES",    # Spanish               Spain 
    "et_EE",    # Estonian              Estonia 
    "fa_IR",    # Persian               Iran 
    "fi_FI",    # Finnish               Finland 
    "fil_PH",   # Filipino              Philippines 
    "fj_FJ",    # Fijian                Fiji
    "fo_FO",    # Faroese               Faeroe Islands
    "fon_BJ",   # Fon                   Benin 
    "fr_FR",    # French                France 
    "fy_NL",    # Western Frisian       Netherlands 
    "ga_IE",    # Irish                 Ireland 
    "gd_GB",    # Scots                 Britain 
    "gon_IN",   # Gondi                 India 
    "gsw_CH",   # Swiss German          Switzerland 
    "gu_IN",    # Gujarati              India 
    "he_IL",    # Hebrew                Israel 
    "hi_IN",    # Hindi                 India 
    "hil_PH",   # Hiligaynon            Philippines 
    "hr_HR",    # Croatian              Croatia 
    "ht_HT",    # Haitian               Haiti 
    "hu_HU",    # Hungarian             Hungary 
    "hy_AM",    # Armenian              Armenia 
    "id_ID",    # Indonesian            Indonesia 
    "ig_NG",    # Igbo                  Nigeria 
    "ii_CN",    # Sichuan Yi            China 
    "ilo_PH",   # Iloko                 Philippines 
    "is_IS",    # Icelandic             Iceland 
    "it_IT",    # Italian               Italy 
    "ja_JP",    # Japanese              Japan 
    "jab_NG",   # Hyam                  Nigeria 
    "jv_ID",    # Javanese              Indonesia 
    "ka_GE",    # Georgian              Georgia 
    "kab_DZ",   # Kabyle                Algeria 
    "kaj_NG",   # Jju                   Nigeria 
    "kam_KE",   # Kamba                 Kenya 
    "kmb_AO",   # Kimbundu              Angola 
    "kcg_NG",   # Tyap                  Nigeria 
    "kdm_NG",   # Kagoma                Nigeria 
    "kg_CD",    # Kongo                 Democratic Republic of Congo 
    "kk_KZ",    # Kazakh                Kazakhstan 
    "kl_GL",    # Kalaallisut           Greenland 
    "km_KH",    # Khmer                 Cambodia 
    "kn_IN",    # Kannada               India 
    "ko_KR",    # Korean                Korea (South) 
    "kok_IN",   # Konkani               India 
    "kr_NG",    # Kanuri                Nigeria 
    "kru_IN",   # Kurukh                India 
    "lg_UG",    # Ganda                 Uganda 
    "li_BE",    # Limburgish            Belgium 
    "lo_LA",    # Laotian               Laos 
    "lt_LT",    # Lithuanian            Lithuania 
    "lu_CD",    # Luba-Katanga          Democratic Republic of Congo 
    "lua_CD",   # Luba-Lulua            Democratic Republic of Congo 
    "luo_KE",   # Luo                   Kenya 
    "lv_LV",    # Latvian               Latvia 
    "mad_ID",   # Madurese              Indonesia 
    "mag_IN",   # Magahi                India 
    "mai_IN",   # Maithili              India 
    "mak_ID",   # Makasar               Indonesia 
    "man_ML",   # Mandingo              Mali 
    "men_SL",   # Mende                 Sierra Leone 
    "mg_MG",    # Malagasy              Madagascar 
    "min_ID",   # Minangkabau           Indonesia 
    "mk_MK",    # Macedonian            Macedonia 
    "ml_IN",    # Malayalam             India 
    "mn_MN",    # Mongolian             Mongolia 
    "mni_IN",   # Manipuri              India 
    "mos_BF",   # Mossi                 Burkina Faso 
    "mr_IN",    # Marathi               India 
    "ms_MY",    # Malay                 Malaysia 
    "mt_MT",    # Maltese               Malta 
    "mwr_IN",   # Marwari               India 
    "my_MM",    # Burmese               Myanmar 
    "na_NR",    # Nauru                 Nauru 
    "nah_MX",   # Nahuatl               Mexico 
    "nap_IT",   # Neapolitan            Italy 
    "nb_NO",    # Norwegian Bokmål      Norway 
    "nds_DE",   # Low Saxon             Germany 
    "ne_NP",    # Nepali                Nepal 
    "nl_NL",    # Dutch                 Netherlands 
    "nn_NO",    # Norwegian Nynorsk     Norway 
    "no_NO",    # Norwegian             Norway 
    "nr_ZA",    # South Ndebele         South Africa 
    "nso_ZA",   # Northern Sotho        South Africa 
    "nym_TZ",   # Nyamwezi              Tanzania 
    "nyn_UG",   # Nyankole              Uganda 
    "oc_FR",    # Occitan               France 
    "oj_CA",    # Ojibwa                Canada 
    "or_IN",    # Oriya                 India 
    "pa_IN",    # Punjabi               India 
    "pag_PH",   # Pangasinan            Philippines 
    "pam_PH",   # Pampanga              Philippines 
    "pbb_CO",   # Páez                  Colombia 
    "pl_PL",    # Polish                Poland 
    "ps_AF",    # Pashto                Afghanistan 
    "pt_PT",    # Portuguese            Portugal 
    "raj_IN",   # Rajasthani            India 
    "rm_CH",    # Rhaeto-Roman          Switzerland 
    "rn_BI",    # Kirundi               Burundi 
    "ro_RO",    # Romanian              Romania 
    "ru_RU",    # Russian               Russia 
    "sa_IN",    # Sanskrit              India 
    "sas_ID",   # Sasak                 Indonesia 
    "sat_IN",   # Santali               India 
    "sc_IT",    # Sardinian             Italy 
    "scn_IT",   # Sicilian              Italy 
    "sg_CF",    # Sango                 Central African Republic 
    "shn_MM",   # Shan                  Myanmar 
    "si_LK",    # Sinhala               Sri Lanka 
    "sid_ET",   # Sidamo                Ethiopia 
    "sk_SK",    # Slovak                Slovakia 
    "sl_SI",    # Slovenian             Slovenia 
    "so_SO",    # Somali                Somalia 
    "sq_AL",    # Albanian              Albania 
    "sr_RS",    # Serbian               Serbia 
    "sr_YU",    # Serbian               Yugoslavia 
    "srr_SN",   # Serer                 Senegal 
    "suk_TZ",   # Sukuma                Tanzania 
    "sus_GN",   # Susu                  Guinea 
    "sv_SE",    # Swedish               Sweden 
    "te_IN",    # Telugu                India 
    "tem_SL",   # Timne                 Sierra Leone 
    "tet_ID",   # Tetum                 Indonesia 
    "tg_TJ",    # Tajik                 Tajikistan 
    "th_TH",    # Thai                  Thailand 
    "tiv_NG",   # Tiv                   Nigeria 
    "tk_TM",    # Turkmen               Turkmenistan 
    "tl_PH",    # Tagalog               Philippines 
    "to_TO",    # Tonga                 Tonga 
    "tr_TR",    # Turkish               Turkey 
    "tum_MW",   # Tumbuka               Malawi 
    "uk_UA",    # Ukrainian             Ukraine 
    "umb_AO",   # Umbundu               Angola 
    "ur_PK",    # Urdu                  Pakistan 
    "uz_UZ",    # Uzbek                 Uzbekistan 
    "ve_ZA",    # Venda                 South Africa 
    "vi_VN",    # Vietnamese            Vietnam 
    "wa_BE",    # Walloon               Belgium 
    "wal_ET",   # Walamo                Ethiopia 
    "war_PH",   # Waray                 Philippines 
    "wen_DE",   # Sorbian               Germany 
    "yao_MW",   # Yao                   Malawi 
    "zap_MX"    # Zapotec               Mexico 
)
