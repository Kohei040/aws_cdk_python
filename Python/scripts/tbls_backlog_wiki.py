import requests
import json
import glob
import os
import re

BACKLOG_HOST = 'https://xxxxx.backlog.com'
BACKLOG_API_KEY = 'xxxxxxxx'
project_id = xxxx

contents_path = './output'
wiki_prefix_page_name = 'テーブル定義書'


def main():
    """
    tblsで取得したDBドキュメント(md, png)をBacklog Wikiに反映する
    コンテンツを格納するディレクトリ構成は、[./output/対象instance/対象ファイル(md, png)]とする。
    """

    instance_dir_list = glob.glob(os.path.join(contents_path, './*'))
    for instance_dir in instance_dir_list:
        instance = os.path.split(instance_dir)[1]
        file_path = f'{contents_path}/{instance}'
        # 全てのmdファイル及びpngファイルのパス取得
        md_file_list = glob.glob(os.path.join(file_path, './*.md'))
        for md_file_path in md_file_list:
            md_file = os.path.split(md_file_path)[1]
            # Wikiページの名前を決定
            wiki_page_name = check_table_definition(instance, md_file)
            # WikiページのIDを取得、ページが存在しなければ作成
            wiki_page_id = (add_wiki_page(wiki_page_name)
                            if not (exist_id :=check_exist_page(wiki_page_name))
                            else exist_id)
            # Wikiページにある旧添付ファイルを削除
            [delete_wiki_file(wiki_page_id, i)
             for i in get_wiki_file(wiki_page_id)]

            png_file_name = (md_file.replace('.md', '.png')
                             if md_file != 'README.md' else 'schema.png')
            png_file_path = f'{file_path}/{png_file_name}'
            # Backlogにファイル送信
            backlog_file_id = upload_file_to_backlog(png_file_path,
                                                     png_file_name)
            # 送信したファイルをWikiページにアタッチ
            wiki_file_id = attach_wiki_file(wiki_page_id, backlog_file_id)
            # 画像リンクの修正
            with open(md_file_path, 'r', encoding='utf-8') as f:
                ori_md_content = f.read()
            wiki_content = re.sub(f'\({png_file_name}\)',
                                  f'[{wiki_file_id}]',
                                  ori_md_content)
            # Wikiページに反映
            update_wiki_page(wiki_page_id,
                             wiki_page_name,
                             wiki_content)


def check_table_definition(instance, md_file):
    """
    コンテンツがテーブル定義かどうかを判断し、Wikiページ名を決定する。
    README.md   -> {wiki_prefix_page_name}/インスタンス名
    テーブル定義 -> {wiki_prefix_page_name}/インスタンス名/テーブル名

    Parameters
    ----------
    instance: str
        収集対象のインスタンス名。
    md_file: list
        Wikiのコンテンツとなるmdファイルの一覧。

    Returns
    ----------
    wiki_page_name: str
        Wikiページの名前。
    """

    if md_file == 'README.md':
        wiki_page_name = f'{wiki_prefix_page_name}/{instance}'
    else:
        table = md_file.replace('.md', '')
        wiki_page_name = f'{wiki_prefix_page_name}/{instance}/{table}'

    return wiki_page_name


def check_exist_page(wiki_page_name):
    """
    Wikiページが既に存在しているかを確認。

    Parameters
    ----------
    wiki_page_name: str
        Wikiページの名前。

    Returns
    ----------
    wiki_page_id: int
        WikiページのID。0の場合、Wikiページは存在しない。
    """
    existing_wiki = get_wiki_page_list()
    if wiki_page_name in existing_wiki.keys():
        print(f'{wiki_page_name}は既に存在しています。')
        wiki_page_id = existing_wiki[wiki_page_name]
        return wiki_page_id
    else:
        print(f'{wiki_page_name}を新規作成します。')
        wiki_page_id = ""
        return wiki_page_id


def get_wiki_page_list():
    """
    Backlog Wikiのページ一覧を取得する。

    Returns
    -------
    wiki_page_dict: dict
        Wikiページの一覧を{ページ名: ID}で格納
    """
    payload = {
        'apiKey': BACKLOG_API_KEY,
        'projectIdOrKey': project_id,
    }
    wiki_page_list = requests.get(BACKLOG_HOST + '/api/v2/wikis',
                                  params=payload).json()
    wiki_page_ids = [i['id'] for i in wiki_page_list]
    wiki_page_names = [i['name'] for i in wiki_page_list]
    wiki_page_dict = dict(zip(wiki_page_names, wiki_page_ids))

    return wiki_page_dict


def add_wiki_page(wiki_page_name):
    """
    Wikiページを新規作成する。

    Parameters
    ----------
    wiki_page_name: str
        Wikiページの名前。
    """

    payload = {
        'apiKey': BACKLOG_API_KEY,
        'projectId': project_id,
        'name': wiki_page_name,
        'content': wiki_page_name,
    }
    url = f'{BACKLOG_HOST}/api/v2/wikis'
    try:
        add_wiki_page_req = requests.post(url, params=payload).json()
        wiki_page_id = add_wiki_page_req['id']
        return wiki_page_id
    except Exception as e:
        print(e)


def get_wiki_file(wiki_page_id):
    """
    既存のWiki添付ファイルを取得する。

    Parameters
    ----------
    wiki_page_id: int
        WikiページのID

    Returns
    ----------
    wiki_file_ids : int
        Wiki添付ファイルのID。
    """

    payload = {
        'apiKey': BACKLOG_API_KEY,
    }
    url = f'{BACKLOG_HOST}/api/v2/wikis/{str(wiki_page_id)}/attachments'
    # Wiki添付ファイルの一覧を取得
    try:
        wiki_file_list = requests.get(url, params=payload).json()
        wiki_file_ids = [i['id'] for i in wiki_file_list]
        return wiki_file_ids
    except Exception as e:
        print(e)


def delete_wiki_file(wiki_page_id, wiki_file_id):
    """
    wiki添付ファイルを削除する。

    Parameters
    ----------
    wiki_page_id: int
        wikiページのID。
    wiki_file_id: int
        wiki添付ファイルのID。
    """

    payload = {
        'apiKey': BACKLOG_API_KEY,
    }
    url = f'{BACKLOG_HOST}/api/v2/wikis/{wiki_page_id}/attachments/{wiki_file_id}'
    try:
        delete_wiki_file_req = requests.delete(url, params=payload).json()
    except Exception as e:
        print(e)


def upload_file_to_backlog(png_file_path, png_file_name):
    """
    Backlogにファイルを送信する。

    Parameters
    ----------
    png_file_path : str
        送信するファイルのパス。
    png_file_name : str
        送信するファイル名。
    """

    payload = {
        'apiKey': BACKLOG_API_KEY,
    }
    upload_file = {'file': (png_file_name,
                            open(png_file_path, 'rb'),
                            'image/png')}
    url = f'{BACKLOG_HOST}/api/v2/space/attachment'
    try:
        upload_file_to_backlog_req = requests.post(url, params=payload,
                                                   files=upload_file).json()
        send_file_id = upload_file_to_backlog_req['id']
        return send_file_id
    except Exception as e:
        print(e)


def attach_wiki_file(wiki_page_id, backlog_file_id):
    """
    Backlogに送信したファイルをWikiに添付する。

    Parameters
    ----------
    wiki_page_id: int
        wikiページのID。
    backlog_file_id: int
        Backlogに送信したファイルのID。

    Returns
    ----------
    wiki_file_id: int
        wikiに添付したファイルのID
    """

    payload = {
        'apiKey': BACKLOG_API_KEY,
        'attachmentId[]': backlog_file_id,
    }
    url = f'{BACKLOG_HOST}/api/v2/wikis/{wiki_page_id}/attachments'
    try:
        attach_wiki_file_req = requests.post(url, params=payload).json()
        wiki_file_id = attach_wiki_file_req[0]['id']
        return wiki_file_id
    except Exception as e:
        print(e)


def update_wiki_page(wiki_page_id, wiki_page_name, wiki_content):
    """
    Wikiページを新規作成する。

    Parameters
    ----------
    wiki_page_id: int
        WikiページのID。
    wiki_page_name: str
        Wikiページの名前。
    wiki_content: str
        Wikiページのコンテンツ。
    """

    payload = {
        'apiKey': BACKLOG_API_KEY,
        'name': wiki_page_name,
        'content': wiki_content,
    }
    url = f'{BACKLOG_HOST}/api/v2/wikis/{wiki_page_id}'
    try:
        update_wiki_page_req = requests.patch(url, params=payload).json()
        result_req_str = json.dumps(update_wiki_page_req)
        if 'errors' in result_req_str:
            print('Wikiの更新に失敗しました。')
            update_wiki_page_req_str = json.dumps(update_wiki_page_req)
            with open('./response.json', 'a', encoding='utf-8') as f:
                f.write(f'{wiki_page_name}\n'
                        f'{update_wiki_page_req_str}\n'
                        f'{wiki_content}\n\n')
        else:
            print('Wikiの更新が完了しました。')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
