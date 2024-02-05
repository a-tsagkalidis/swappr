import json
from random import choice, randint
from fSQL import create_database_tables
from fictional_names import name_generator
from fhelpers import cursor_execute, cursor_fetch


def round_rental(number):
    '''
    Rounds rental to the closest decade
    '''
    return round(number, -1)


def generate_user(id_increment, existing_names):
    '''
    Returns a dictionary of a randomly generated user. Duplicated names
    are prevented thanks to a set of existing_names that is imported
    as an argument. In case a name exists, then a suffix increment number
    is added to the name string for uniqueness.
    '''
    names = name_generator.generate_name

    while True:
        # Create a name for the mockup user entry
        name = names(
            gender=choice(['male', 'female']),
            style='english',
            library=False
        ).replace(" ", ".").lower()
        
        # Check if the generated name is unique
        if name not in existing_names:
            existing_names.add(name)
            break
        else:
            # Append a unique suffix to the name
            suffix = 1970 + randint(0, 36)
            new_name = f"{name}{suffix}"
            while new_name in existing_names:
                suffix += 1
                new_name = f"{name}{suffix}"
                
            name = new_name
            existing_names.add(name)
            break
    
    return {
        'user_id': id_increment + 1,
        'username': name.replace('.', ''),
        'email': f"{name}@swappr.com"
    }


def create_mockups(
        GENERATED_USERS,
        GENERATED_SUBMISSIONS
):
    '''
    Define the number of mockup users and submissions you want to create
    '''
    # A list of valid house types, square meters, bedrooms, bathrooms,
    # exposure, and primary submission statuses to be declared in the mockup
    # submission entry
    house_type = [
        'studio',
        'flat',
        'maisonette',
        'semi-detached_house',
        'detached_house',
        'mansion'
    ]
    square_meters = [i for i in range(30, 160)]
    rental = [ i for i in range(300, 1200)]
    bedrooms = [i for i in range(1, 4)]
    bathrooms = [i for i in range(1, 2)]
    exposure = 'public'
    primary_submission = 1

    # Create a list that will store the generated mockup user entries. List
    # already has stored by default `admin` user for testing purposes
    users = [
        {
            'user_id': 1,
            'username': 'admin',
            'email': 'admin@swappr.com'
        }
    ]

    # Declare a set where generated names are stored to prevent duplicates
    generated_names = set()

    # Append the generated mockup user entries in the users list
    for id in range(1, GENERATED_USERS):
        user_data = generate_user(id, generated_names)
        users.append(user_data)

    # Convert and store the mockup users list into a JSON file
    json_data = json.dumps(users, indent=4)
    with open('tmockusers.json', 'w') as f:
        f.write(json_data)

    # Create a list of dicts with all the valid locations; data is copied
    # from `locations.json`
    locations = [
        {
            "id": 1,
            "city": "thessaloniki",
            "municipality": "thessaloniki",
            "region": {
                "agia_aikaterini": "54632",
                "agia_sofia": "54623",
                "agia_triada": "54639",
                "agioi_anargyroi": "54634",
                "agioi_pantes_-_strofi_eptalofou": "54627",
                "agios_nikolaos_orfanos": "54634",
                "analipsi": "54643",
                "ano_poli": "54633",
                "ano_toumpa": "54351",
                "armenika": "54627",
                "afrodision": "54643",
                "axios": "56727",
                "vardaris": "54626",
                "vlatadon": "54634",
                "vosporos": "54627",
                "voulgari": "54248",
                "vrysaki": "54644",
                "gefyrakia": "54627",
                "delfon": "54645",
                "dioikitirio": "54631",
                "ekklisiastiki_scholi": "54250",
                "eptapyrgio": "54634",
                "ergatikes_katikoies_xirokrinis": "54629",
                "evzonon_-_gallikos_institouto": "54639",
                "eukleidis": "54639",
                "ippokrateio": "54642",
                "ichthyoskala_-_sfageia_-_fix": "54627",
                "kaoudi": "54248",
                "kastra": "54633",
                "kato_toumpa": "54453",
                "kineziki_agora": "54629",
                "kifisia": "54248",
                "kolomvou_-_palio_dimarcheio": "54626",
                "koule_kafe": "54634",
                "kritis": "54646",
                "kybeleia": "54641",
                "lachanokipoi": "54627",
                "lefkos_pyrgos_-_ippodromos": "54621",
                "limani": "54625",
                "malakopi": "54454",
                "mpalta": "54627",
                "nea_elvetia": "54249",
                "nea_paralia": "54642",
                "neos_sidirodromikos_stathmos_-_zografoy": "54627",
                "ntepo": "54655",
                "xirokrini": "54629",
                "osios_david": "54633",
                "palia_lachanogora": "54632",
                "palia_salamina": "54643",
                "palios_sidirodromikos_stathmos": "54627",
                "panagia_faneromeni": "54632",
                "papafeio": "54638",
                "platanos": "54634",
                "plateia_mina_patrikiou": "54248",
                "portara": "54634",
                "poseidonio": "54646",
                "profitis_ilias": "54633",
                "ramona": "54629",
                "rema_yphanet": "54639",
                "saranta_ekklisies": "54636",
                "trochiodromikon": "54250",
                "tsinari": "54633",
                "faliro": "54642",
                "fragkomachalas": "54625",
                "charilaou": "54250"
            }
        },
        {
            "id": 2,
            "city": "thessaloniki",
            "municipality": "agios_pavlos",
            "region": {
                "evagelistria": "55437"
            }
        },
        {
            "id": 3,
            "city": "thessaloniki",
            "municipality": "ampelokipoi",
            "region": {
                "axios": "56727",
                "dimarcheio": "56123",
                "eptalofos_-_filippou": "56121",
                "zoodochos_pigi": "56121",
                "kaistri": "56123",
                "metagogon": "56123",
                "xirokrini": "56123",
                "skeparni": "56123"
            }
        },
        {
            "id": 4,
            "city": "thessaloniki",
            "municipality": "eleftherio_-_kordelio",
            "region": {
                "viotechniki_periochi_-_sidirodromiko_parko": "56334",
                "dialogi": "56334"
            }
        },
        {
            "id": 5,
            "city": "thessaloniki",
            "municipality": "efkarpia",
            "region": {
                "ergatikes_katoikies_-_makedonia": "56429",
                "efxinoupoli": "56450",
                "efedroupoli_pavlou_mela": "56450",
                "nikopoli": "56429"
            }
        },
        {
            "id": 6,
            "city": "thessaloniki",
            "municipality": "evosmos",
            "region": {
                "agioi_kyrillos_kai_methodios": "56224",
                "agios_athanasios": "56224",
                "agios_kosmas": "56225",
                "anos_evosmos": "56226",
                "anothen_periferiakou": "56238",
                "evagelismos_-_neos_koulkoutzas": "56224",
                "efxinoupoli": "56450",
                "kato_evosmos": "56225",
                "kato_ilioupoli": "56224"


            }
        },
        {
            "id": 7,
            "city": "thessaloniki",
            "municipality": "thermi",
            "region": {
                "agios_tryfonas": "57001",
                "triadi": "57001"
            }
        },
        {
            "id": 8,
            "city": "thessaloniki",
            "municipality": "kalamaria",
            "region": {
                "agios_ioannis": "55132",
                "agios_stylianos": "55134",
                "aretsou": "55132",
                "votsi": "55134",
                "vyzantio": "55133",
                "derkon": "55132",
                "ergatikes_katikoies_foinika": "55135",
                "karampournaki": "55131",
                "katirli": "55132",
                "kentro": "55133",
                "kifisia": "55133",
                "kouri": "55132",
                "nea_krini": "55132",
                "ntepo": "55131"
            }
        },
        {
            "id": 9,
            "city": "thessaloniki",
            "municipality": "menemeni",
            "region": {
                "vosporos": "54628",
                "dendropotamos": "54628",
                "lachanagora": "54628",
                "lachanokipoi": "54628",
                "paralia_dendropotamou": "54628"
            }
        },
        {
            "id": 10,
            "city": "thessaloniki",
            "municipality": "neapoli",
            "region": {
                "anagennisi": "56727",
                "axios": "56727",
                "valsami": "56728",
                "kalithea": "56728",
                "kokkoras": "56728",
                "kolokotroni": "56728",
                "nea_varna": "56728",
                "paraschou": "56728",
                "proin_stratopedo_strempenioti": "56728",
                "pyropathon": "56727",
                "troada_-_agios_georgios": "56728"
            }
        },
        {
            "id": 11,
            "city": "thessaloniki",
            "municipality": "sykies",
            "region": {
                "agios_vasileios": "56625",
                "agios_charalampos": "56626",
                "akrites": "56625",
                "dendrofyteia_-_alsos_sykeon": "56626",
                "eptapyrgio": "56626",
                "kalithea": "56625",
                "kastra": "54634",
                "panagia_faneromeni": "56625",
                "paraschou": "56626",
                "rodochori_-_armenochori": "56626",
                "tzitzifies": "56625"
            }
        },
        {
            "id": 12,
            "city": "thessaloniki",
            "municipality": "panorama",
            "region": {
                "ano_panorama": "55236",
                "neo_panorama": "55236",
                "oikismos_efedron_aksiomatikon_makedonia": "55236",
                "plateia_mpakogianni": "55236",
                "topografoi": "55236"
            }
        },
        {
            "id": 13,
            "city": "thessaloniki",
            "municipality": "polichni",
            "region": {
                "agios_panteleimonas": "56533",
                "analipsi_-_ano_polichni": "56533",
                "anthokipoi": "56429",
                "ano_meteora_-_agios_rafail": "56532",
                "elpida": "56533",
                "kokkoras": "56626",
                "kountourioti": "56533",
                "meteora": "56532",
                "neromyloi": "56532",
                "nikopoli": "56535",
                "oikismos_megalou_alexandroy": "56533",
                "ydragogeio_-_agios_ioannis": "56532"
            }
        },
        {
            "id": 14,
            "city": "thessaloniki",
            "municipality": "pylaia",
            "region": {
                "elaiorema": "55534",
                "elaiones": "55536",
                "kypseli": "55535",
                "konstantinoupolitika": "55534",
                "malakopi": "55534",
                "patriarchiko": "55535",
                "pylaiotika": "55535",
                "rema": "55535",
                "samarakia": "55535",
                "stageiriti": "55534",
                "topografoi": "55536"
            }
        },
        {
            "id": 15,
            "city": "thessaloniki",
            "municipality": "stavroupoli",
            "region": {
                "ampelones": "56430",
                "anthokipoi": "56535",
                "ano_ilioupoli": "56431",
                "anothen_asylou": "56436",
                "kato_ilioupoli": "56431",
                "neoktista": "56436",
                "nikopoli": "56437",
                "omonoia": "56430",
                "pronoia": "56430",
                "terpsithea": "56430"
            }
        },
        {
            "id": 16,
            "city": "thessaloniki",
            "municipality": "triandria",
            "region": {
                "agioi_anargyroi": "55337",
                "ano_triandria": "55337",
                "kato_triandria": "55337"
            }
        },
        {
            "id": 17,
            "city": "thessaloniki",
            "municipality": "epanomi",
            "region": {
                "pyrgos": "57500"
            }
        },
        {
            "id": 18,
            "city": "larissa",
            "municipality": "larissa",
            "region": {
                "averof": "41335",
                "agia_marina": "41336",
                "agia_paraskevi": "41334",
                "agioi_saranta": "41221",
                "agios_athanasios": "41222",
                "agios_achileios": "41223",
                "agios_georgios": "41336",
                "agios_thomas": "41334",
                "agios_konstantinos": "41221",
                "agios_nikolaos": "41223",
                "alkazar": "41447",
                "ampelokipoi": "41447",
                "anatoli": "41336",
                "anthoupoli": "41335",
                "emporiko_parko_ag._marinas": "41336",
                "exi dromoi": "41222",
                "ergatikes_katikoies_neapolis": "41334",
                "ipeirotika": "41335",
                "ippokratis": "41447",
                "kazantzidika": "41222",
                "lachanokipoi": "41336",
                "livadaki": "41334",
                "nea_ekali_-_lofaki": "41335",
                "nea_politeia": "41335",
                "nea_smyrni": "41336",
                "neapoli": "41334",
                "neraida": "41334",
                "palia_evraiki_synoikia": "41222",
                "papastavrou": "41447",
                "potamopoli": "41334",
                "pyrovolika": "41335",
                "sidirodromikos_stathmos": "41335",
                "toumpa": "41448",
                "filippoupoli": "41334",
                "xaravgi": "41448"
            }
        },
        {
            "id": 19,
            "city": "larissa",
            "municipality": "tyrnavos",
            "region": {
                "ampelonas": "41335",
                "vriotopos": "41336"
            }
        },
        {
            "id": 20,
            "city": "xanthi",
            "municipality": "xanthi",
            "region": {
                "mexicana": "41335",
                "plateia": "41336",
                "chrysa": "41334",
                "ektenopol": "41221"
            }
        }
    ]

    # Declare an empty list where the generated submissions will be stored
    data = []

    # Declare an empty set where the users that already submitted a house
    # will be stored
    used_users = set()
    for i in range(GENERATED_SUBMISSIONS):
        # Create dictionaries to map cities to their corresponding municipalities
        # and regions for both source and destination
        random_location = choice(locations)
        random_destination = choice(locations)

        city_mapping_source = {
            random_location['city']: {
                random_location['municipality']: random_location['region']
            }
        }
        city_mapping_destination = {
            random_destination['city']: {
                random_destination['municipality']: random_destination['region']
            }
        }

        # Generate valid location data for source
        city_source = choice(list(city_mapping_source.keys()))
        municipality_region_mapping_source = city_mapping_source[city_source]
        municipality_source = choice(list(municipality_region_mapping_source.keys()))
        region_mapping_source = municipality_region_mapping_source[municipality_source]
        region_source = choice(list(region_mapping_source.keys()))
        postal_code_source = region_mapping_source[region_source]

        # Generate valid location data for destination
        city_destination = choice(
            list(
                city_mapping_destination.keys()
            )
        )
        municipality_region_mapping_destination = city_mapping_destination[city_destination]
        municipality_destination = choice(
            list(
                municipality_region_mapping_destination.keys()
            )
        )
        region_mapping_destination = municipality_region_mapping_destination[municipality_destination]
        region_destination = choice(
            list(
                region_mapping_destination.keys()
            )
        )
        
        # Select a random user who will own the generated submission
        random_user = choice(users)
        # Prevent the user from owning more than one submission
        while True:
            if random_user['username'] not in used_users:
                used_users.add(random_user['username'])
                break
            else:
                random_user = choice(users)

        # Generate mockup submission entry and store it in data list
        entry = {
            "bathrooms": choice(bathrooms),
            "bedrooms": choice(bedrooms),
            "city": city_source,
            "city_destination": city_destination,
            "email": random_user['email'],
            "exposure": exposure,
            "house_type": choice(house_type),
            "id": i + 1,
            "municipality": municipality_source,
            "municipality_destination": municipality_destination,
            "postal_code": postal_code_source,
            # "postal_code_destination": postal_code_destination,
            "primary_submission": primary_submission,
            "region": region_source,
            "region_destination": region_destination,
            "rental": round_rental(choice(rental)),
            "square_meters": choice(square_meters),
            "user_id": random_user['user_id'],
            "username": random_user['username']
        }
        data.append(entry)

    # Convert and store the mockup users list into a JSON file
    json_data = json.dumps(data, indent=4)
    with open('tmocksubmissions.json', 'w') as f:
        f.write(json_data)


def load_mockup_submissions():
    '''
    TODO Docstring
    '''
    create_database_tables()

    with open('tmocksubmissions.json', 'r') as json_file:
        submissions = json.load(json_file)

        query = '''
                INSERT INTO submissions (
                    user_id,
                    house_type,
                    square_meters,
                    rental,
                    bedrooms,
                    bathrooms,
                    city,
                    municipality,
                    region,
                    city_destination,
                    municipality_destination,
                    region_destination,
                    exposure,
                    primary_submission
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                '''

        for submission in submissions:
            cursor_execute(
                query,
                submission['user_id'],
                submission['house_type'],
                submission['square_meters'],
                submission['rental'],
                submission['bedrooms'],
                submission['bathrooms'],
                submission['city'],
                submission['municipality'],
                submission['region'],
                submission['city_destination'],
                submission['municipality_destination'],
                submission['region_destination'],
                submission['exposure'],
                submission['primary_submission']
            )


def load_mockup_users():
    '''
    TODO Docstring
    '''
    create_database_tables()

    with open('tmockusers.json', 'r') as json_file:
        users = json.load(json_file)

        query = '''
                INSERT INTO users (
                    id,
                    username,
                    email,
                    hash,
                    registration_date,
                    verified_account
                )
                VALUES (?, ?, ?, ?, ?, ?);
                '''

        for user in users:
            cursor_execute(
                query,
                user['user_id'],
                user['username'],
                user['email'],
                'scrypt:32768:8:1$qICfKjC9CagbVSrn$efd605af1c704a9ba1ac242acad6e8a49d7568d60aa9028e54271d94a69ecc0ebfa75a56c9278a48db227e1b685337bba53c1170a5b6016ba7336083a8bd259c',
                '2024-02-03 09:38:41.231061',
                0
            )


def insert_mockups(
        GENERATED_USERS,
        GENERATED_SUBMISSIONS
):
    '''
    Runs tload_mockusers.py and tload_mocksubmissions.py in case the
    database corresponding tables are empty. The scripts are loading
    mockups that are stored in tmockusers.json and tmocksubmisssions.json
    respectively.
    '''
    tables_checklist = [
        'users',
        'submissions'
    ]
    counts = []
    for table in tables_checklist:
        query = f'''
                SELECT COUNT(*) FROM {table};
                '''
        counts.append(cursor_fetch(query)[0]['COUNT(*)'])
    
    if counts[0] == 0 and counts[1] == 0:
        create_mockups(GENERATED_USERS, GENERATED_SUBMISSIONS)
        load_mockup_users()
        load_mockup_submissions()
        