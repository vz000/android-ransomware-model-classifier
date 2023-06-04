import rust
from static.static_classify import *
from dynamic.dynamic_classify import *
from parse import *

def launch(apk_path: str) -> dict:
    parse_static_data(apk_path)
    classify = static_classify('./out/permissions.csv',3)
    static_results = classify.classify()
    rust.start_analysis(apk_path)
    get_freq_list = [parse_freq_data("ransomware"),parse_freq_data("goodware")]
    parsed_out = parse_dynamic_data()
    dynamic_result = dynamic_classify(parsed_out.parsed_logs(), get_freq_list)
    result = {
            'name': static_results['name'],
            'static': static_results['static'] ,
            'dynamic': dynamic_result['dynamic']
    }
    return result
