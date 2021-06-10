import os
import re
import json
from accented_unaccented_mapper import accented_unaccented_map
from concurrent.futures import ThreadPoolExecutor, as_completed


def return_without_accented_chars(accented_string):
    split_string = list(accented_string)
    for i, char in enumerate(split_string):
        if accented_unaccented_map.get(char) is not None:
            split_string[i] = accented_unaccented_map.get(char)
        if split_string[i] != " " and not split_string[i].isalnum():
            split_string[i] = ""

    unaccented_string = ''.join(split_string)

    return unaccented_string


def get_impact_factor(title):
    title = return_without_accented_chars(title)
    journal_name = '+'.join(title.split(' '))
    google_search_command = "curl -s 'https://www.google.com/search?q=impact+factor+of+" + journal_name + "&ei=cmTAYLSEI9Paz7sPsvOoiAU&oq=impact+factor+of+brain+informatics&gs_lcp=Cgdnd3Mtd2l6EAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsANQAFgAYL9ZaAFwAngAgAF6iAF6kgEDMC4xmAEAqgEHZ3dzLXdpesgBCMABAQ&sclient=gws-wiz&ved=0ahUKEwi0hdXl-onxAhVT7XMBHbI5ClEQ4dUDCBI&uact=5' \
        -H 'authority: www.google.com' \
        -H 'sec-ch-ua: \" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"' \
        -H 'sec-ch-ua-mobile: ?0' \
        -H 'upgrade-insecure-requests: 1' \
        -H 'dnt: 1' \
        -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36' \
        -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
        -H 'sec-fetch-site: same-origin' \
        -H 'sec-fetch-mode: navigate' \
        -H 'sec-fetch-user: ?1' \
        -H 'sec-fetch-dest: document' \
        -H 'referer: https://www.google.com/' \
        -H 'accept-language: en-US,en;q=0.9' \
        -H 'cookie: NID=216=q06epUihWttLRaLM6XYKlWJbL752Z0XPIGUdtbmoZdiYUyBujfOq_TsUxrnMgEECIyP8rrY5k49Kcs53DUcU38odfsX9KJv0W_sNwCs6_3NAC7SiyRRQPaF6m0QWdoRhMTj9F-esb1JATlhGp_yUYukDgAqBfZcCjgRXeRr7vk0' \
        --compressed"

    google_resp = os.popen(google_search_command).read()

    pattern = r'data-tts-text=\"([0-9.]*)\"'
    result = re.search(pattern, google_resp)
    if result:
        impact_factor = str(result.group(1))
    else:
        impact_factor = "None"

    resurchify_search_command = "curl -s 'https://www.resurchify.com/find/?query=" + journal_name + "' \
          -H 'authority: www.resurchify.com' \
          -H 'cache-control: max-age=0' \
          -H 'sec-ch-ua: \" Not;A Brandd\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"' \
          -H 'sec-ch-ua-mobile: ?0' \
          -H 'dnt: 1' \
          -H 'upgrade-insecure-requests: 1' \
          -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36' \
          -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
          -H 'sec-fetch-site: none' \
          -H 'sec-fetch-mode: navigate' \
          -H 'sec-fetch-user: ?1' \
          -H 'sec-fetch-dest: document' \
          -H 'accept-language: en-US,en;q=0.9,hi;q=0.8' \
          -H 'cookie: _ga=GA1.2.1171529541.1623217392; _gid=GA1.2.1406124227.1623217392; __gads=ID=db5b88862c739b87-227e43c347c90051:T=1623217393:RT=1623217393:S=ALNI_Ma1j9fnh2FaAuyL4MFQjBY924HdVw; PHPSESSID=vkhiglbqkapnhn9o1tjpv33064; FCCDCF=[null,null,[\"[[],[],[],[],null,null,true]\",1623255200766],null,null]' \
          --compressed"

    surchify_resp = os.popen(resurchify_search_command).read()

    pattern = r' Impact Score: \"([0-9.]*)\"'
    result_1 = re.search(pattern, surchify_resp)
    if result_1:
        impact_factor_1 = str(result_1.group(1))
    else:
        impact_factor_1 = "None"

    print(title + "," + impact_factor + "," + impact_factor_1)


first_results_command = "curl 'https://www.doaj.org/query/journal/_search?ref=public_journal&source=%7B%22query%22%3A%7B%22filtered%22%3A%7B%22filter%22%3A%7B%22bool%22%3A%7B%22must%22%3A%5B%7B%22term%22%3A%7B%22bibjson.apc.has_apc%22%3Afalse%7D%7D%2C%7B%22term%22%3A%7B%22bibjson.other_charges.has_other_charges%22%3Afalse%7D%7D%2C%7B%22terms%22%3A%7B%22index.language.exact%22%3A%5B%22English%22%5D%7D%7D%2C%7B%22terms%22%3A%7B%22index.schema_codes_tree.exact%22%3A%5B%22LCC%3AL%22%2C%22LCC%3AM%22%2C%22LCC%3AP%22%2C%22LCC%3AQ%22%2C%22LCC%3AR%22%2C%22LCC%3AT%22%2C%22LCC%3AU%22%2C%22LCC%3AZ%22%5D%7D%7D%5D%7D%7D%2C%22query%22%3A%7B%22match_all%22%3A%7B%7D%7D%7D%7D%2C%22size%22%3A%22200%22%2C%22aggs%22%3A%7B%22subject%22%3A%7B%22terms%22%3A%7B%22field%22%3A%22index.schema_codes_tree.exact%22%2C%22size%22%3A9999%2C%22order%22%3A%7B%22_count%22%3A%22desc%22%7D%7D%7D%2C%22year_added%22%3A%7B%22date_histogram%22%3A%7B%22field%22%3A%22created_date%22%2C%22interval%22%3A%22year%22%7D%7D%7D%7D&_=1623310975033' \
  -H 'authority: www.doaj.org' \
  -H 'sec-ch-ua: \" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"' \
  -H 'accept: text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01' \
  -H 'dnt: 1' \
  -H 'x-requested-with: XMLHttpRequest' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-dest: empty' \
  -H 'referer: https://www.doaj.org/search/journals?ref=homepage-box&source=%7B%22query%22%3A%7B%22filtered%22%3A%7B%22filter%22%3A%7B%22bool%22%3A%7B%22must%22%3A%5B%7B%22term%22%3A%7B%22bibjson.apc.has_apc%22%3Afalse%7D%7D%2C%7B%22term%22%3A%7B%22bibjson.other_charges.has_other_charges%22%3Afalse%7D%7D%2C%7B%22terms%22%3A%7B%22index.language.exact%22%3A%5B%22English%22%5D%7D%7D%2C%7B%22terms%22%3A%7B%22index.schema_codes_tree.exact%22%3A%5B%22LCC%3AL%22%2C%22LCC%3AM%22%2C%22LCC%3AP%22%2C%22LCC%3AQ%22%2C%22LCC%3AR%22%2C%22LCC%3AT%22%2C%22LCC%3AU%22%2C%22LCC%3AZ%22%5D%7D%7D%5D%7D%7D%2C%22query%22%3A%7B%22match_all%22%3A%7B%7D%7D%7D%7D%2C%22size%22%3A%22200%22%7D' \
  -H 'accept-language: en-US,en;q=0.9,hi;q=0.8' \
  -H 'cookie: _ga=GA1.2.1399395517.1620889653; _gid=GA1.2.1388237585.1623214290; doaj-cookie-consent=\"By using the DOAJ website you have agreed to our cookie policy.\"' \
  --compressed"

resp = os.popen(first_results_command).read()
data = json.loads(resp)

for j in range(len(data['hits']['hits'])):
    # print(data['hits']['hits'][j]['_source']['index']['title'])
    with ThreadPoolExecutor(max_workers=10) as executor:
        titles = data['hits']['hits'][j]['_source']['index']['title']
        for title in titles:
            executor.submit(get_impact_factor, title)

results_per_page = 200

for i in range(1, 21):
    command = "curl 'https://www.doaj.org/query/journal/_search?ref=public_journal&source=%7B%22query%22%3A%7B%22filtered%22%3A%7B%22filter%22%3A%7B%22bool%22%3A%7B%22must%22%3A%5B%7B%22term%22%3A%7B%22bibjson.apc.has_apc%22%3Afalse%7D%7D%2C%7B%22term%22%3A%7B%22bibjson.other_charges.has_other_charges%22%3Afalse%7D%7D%2C%7B%22terms%22%3A%7B%22index.language.exact%22%3A%5B%22English%22%5D%7D%7D%2C%7B%22terms%22%3A%7B%22index.schema_codes_tree.exact%22%3A%5B%22LCC%3AL%22%2C%22LCC%3AM%22%2C%22LCC%3AP%22%2C%22LCC%3AQ%22%2C%22LCC%3AR%22%2C%22LCC%3AT%22%2C%22LCC%3AU%22%2C%22LCC%3AZ%22%5D%7D%7D%5D%7D%7D%2C%22query%22%3A%7B%22match_all%22%3A%7B%7D%7D%7D%7D%2C%22size%22%3A%22200%22%2C%22from%22%3A200%2C%22aggs%22%3A%7B%22subject%22%3A%7B%22terms%22%3A%7B%22field%22%3A%22index.schema_codes_tree.exact%22%2C%22size%22%3A9999%2C%22order%22%3A%7B%22_count%22%3A%22desc%22%7D%7D%7D%2C%22year_added%22%3A%7B%22date_histogram%22%3A%7B%22field%22%3A%22created_date%22%2C%22interval%22%3A%22year%22%7D%7D%7D%7D&_=1623310975044' \
      -H 'authority: www.doaj.org' \
      -H 'sec-ch-ua: \" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"' \
      -H 'accept: text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01' \
      -H 'dnt: 1' \
      -H 'x-requested-with: XMLHttpRequest' \
      -H 'sec-ch-ua-mobile: ?0' \
      -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36' \
      -H 'sec-fetch-site: same-origin' \
      -H 'sec-fetch-mode: cors' \
      -H 'sec-fetch-dest: empty' \
      -H 'referer: https://www.doaj.org/search/journals?ref=homepage-box&source=%7B%22query%22%3A%7B%22filtered%22%3A%7B%22filter%22%3A%7B%22bool%22%3A%7B%22must%22%3A%5B%7B%22term%22%3A%7B%22bibjson.apc.has_apc%22%3Afalse%7D%7D%2C%7B%22term%22%3A%7B%22bibjson.other_charges.has_other_charges%22%3Afalse%7D%7D%2C%7B%22terms%22%3A%7B%22index.language.exact%22%3A%5B%22English%22%5D%7D%7D%2C%7B%22terms%22%3A%7B%22index.schema_codes_tree.exact%22%3A%5B%22LCC%3AL%22%2C%22LCC%3AM%22%2C%22LCC%3AP%22%2C%22LCC%3AQ%22%2C%22LCC%3AR%22%2C%22LCC%3AT%22%2C%22LCC%3AU%22%2C%22LCC%3AZ%22%5D%7D%7D%5D%7D%7D%2C%22query%22%3A%7B%22match_all%22%3A%7B%7D%7D%7D%7D%2C%22size%22%3A%22200%22%2C%22from%22%3A200%7D' \
      -H 'accept-language: en-US,en;q=0.9,hi;q=0.8' \
      -H 'cookie: _ga=GA1.2.1399395517.1620889653; _gid=GA1.2.1388237585.1623214290; doaj-cookie-consent=\"By using the DOAJ website you have agreed to our cookie policy.\"' \
      --compressed"

    resp = os.popen(command).read()
    data = json.loads(resp)

    for j in range(len(data['hits']['hits'])):
        with ThreadPoolExecutor(max_workers=10) as executor:
            titles = data['hits']['hits'][j]['_source']['index']['title']
            for title in titles:
                executor.submit(get_impact_factor, title)
