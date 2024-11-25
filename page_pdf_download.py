import urllib.request
import requests
from bs4 import BeautifulSoup
import urllib.parse
import tkinter as tk
from tkinter import simpledialog, messagebox
import os
import time
from datetime import datetime
import re


def sanitize_filename(filename):
    # ファイル名に使用できない文字を置換する
    return re.sub(r'[\\/*?:"<>.|]', "_", filename)


def download_pdf(url, save_dir):
    response = requests.get(url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")
    
    a_tags = soup.find_all("a")
    url_list = []  # ダウンロードするPDFのURLリスト
    filename_list = []  # ダウンロードするPDFのファイル名のリスト
    pdf_found = False  # PDF存在フラグ

    # PDFに該当するものだけを絶対パスに変換後、リストへ保存
    for a_tag in a_tags:
        href = a_tag.get("href")
        if href and href.endswith(".pdf"):
            absolute_url = urllib.parse.urljoin(url, href)
            url_list.append(absolute_url)
            filename = sanitize_filename(a_tag.text.strip()) + ".pdf"
            filename_list.append(filename)
            pdf_found = True
    if not pdf_found:        
        messagebox.showerror("エラー", "PDFリンクが見つかりませんでした。")
        return 0

    # 保存ディレクトリを作成
    date_folder = datetime.now().strftime("%Y%m%d%H%M%S")
    save_dir = os.path.join(save_dir, date_folder)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    savepath_list = []  # ダウンロードしたPDFの保存先のリスト
    for filename in filename_list:
        savepath_list.append(os.path.join(save_dir, filename))

    # PDFダウンロード処理
    for (url, savepath) in zip(url_list, savepath_list):
        urllib.request.urlretrieve(url, savepath)
        time.sleep(2)  # サーバ負荷を軽減するための待機
    return len(url_list)


def main():
    root = tk.Tk()
    root.withdraw()
    save_dir = "C:\PDF_download"

    url = simpledialog.askstring("URL入力", "PDFを取得するURLを入力してください。")
    if not url:
        messagebox.showerror("エラー", "URLが入力されていません。")
        return
    try:
        # PDFダウンロードを実行し、ダウンロード数を表示
        num_download = download_pdf(url, save_dir)
        messagebox.showinfo("完了", f"{num_download}個のPDFの保存に成功しました。")
    except Exception as e:
        messagebox.showerror("エラー", f"ダウンロード中にエラーが発生しました。:{e}")


if __name__ == "__main__":
    main()
