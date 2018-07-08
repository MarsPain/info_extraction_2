#-*- coding: utf-8 -*-

import os

from extract.ZengJianChiExtractor import ZengJianChiExtractor


def print_2d_dict(rs_dict):
    if rs_dict is None:
        return
    for (row_id, row) in sorted(rs_dict.items()):
        print(row_id, " => ", sorted(row.items()))


def test_html_parser_table(html_parser, html_file_path):
    for table_dict in html_parser.parse_table(html_file_path):
        print_2d_dict(table_dict)
        print('-' * 80)


def test_html_parser_paragraph(html_parser, html_file_path):
    for paragraph in html_parser.parse_content(html_file_path):
        print(paragraph)


def test_content_extract(zjc_ex):
    paras = [
        "2014年5月27日，本公司接到控股股东彩虹集团电子股份有限公司（以下简称“彩虹电子”）通知，彩虹电子于2014年3月25日通过上海证券交易所大宗交易系统出售了本公司无限售条件流通股股份500万股，占公司股份总数的0.6786%，均价100元；于2014年5月26日通过上海证券交易所大宗交易系统出售了本公司无限售条件流通股股份500万股，占公司股份总数的0.6786%，合计减持1000万股，占公司股份总数的1.357% ",
        "上述两次减持前，彩虹电子持有本公司股份165004798股，占公司股份总数的22.40% ；本次减持后，彩虹电子持有本公司股份155004798股，占公司股份总数的21.04% 。"]
    for record in zjc_ex.extract_from_paragraphs(paras):
        print(record.to_result())
    print(zjc_ex.com_abbr_dict)
    print(zjc_ex.com_full_dict)


#######################################################################################################################


def extract_zengjianchi(zjc_ex, html_dir_path, html_id):
    record_list = []
    for record in zjc_ex.extract(os.path.join(html_dir_path, html_id)):
        if record is not None and record.shareholderFullName is not None and \
                len(record.shareholderFullName) > 1 and \
                record.finishDate is not None and len(record.finishDate) >= 6:
            record_list.append("%s\t%s" % (html_id[:], record.to_result()))

    for record in record_list:
        pass
        # print(record)
    return record_list


def extract_zengjianchi_from_html_dir(zjc_ex, html_dir_path):
    # print('公告id\t股东全称\t股东简称\t变动截止日期\t变动价格\t变动数量\t变动后持股数\t变动后持股比例')
    # with open("result/zengjianchi.txt", "w", encoding="utf-8") as result:
    with open("result/hetong.txt", "w", encoding="utf-8") as result:
        # result.write("公告id\t股东全称\t股东简称\t变动截止日期\t变动价格\t变动数量\t变动后持股数\t变动后持股比例" + "\n")
        result.write("公告id\t甲方\t乙方\t项目名称\t合同名称\t合同金额上限\t合同金额下限\t联合体成员" + "\n")
        for html_id in os.listdir(html_dir_path):
            record_list = extract_zengjianchi(zjc_ex, html_dir_path, html_id)
            for record in record_list:
                result.write(record + "\n")



if __name__ == "__main__":

    # zengjianchi_config_file_path = 'config/ZengJianChiConfig.json'
    zengjianchi_config_file_path = 'config/HeTongConfig.json'
    ner_model_dir_path = './ltp_data_v3.4.0'
    ner_blacklist_file_path = 'config/ner_com_blacklist.txt'

    zjc_ex = ZengJianChiExtractor(zengjianchi_config_file_path, ner_model_dir_path, ner_blacklist_file_path)
    # extract_zengjianchi_from_html_dir(zjc_ex, 'test_data/zengjianchi/html')
    extract_zengjianchi_from_html_dir(zjc_ex, 'test_data/hetong/html')


