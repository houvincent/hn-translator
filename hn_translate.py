#!/usr/bin/env python3
"""
抓取 Hacker News 首页前 20 条新闻，翻译成中文，保存为 Markdown。
"""

from __future__ import annotations

import json
import time
from datetime import date
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

HN_URL = "https://news.ycombinator.com/"
TRANSLATE_API = "https://api.mymemory.translated.net/get"
TOP_N = 20
# 免费 API 容易限流，每条之间稍微停一下（秒）
SLEEP_BETWEEN_TRANSLATIONS = 0.35


def fetch_hn_html(session: requests.Session) -> str:
    """用 requests 下载 HN 首页的 HTML 字符串。"""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    }
    response = session.get(HN_URL, headers=headers, timeout=30)
    response.raise_for_status()
    return response.text


def parse_top_stories(html: str, limit: int) -> list[tuple[str, str]]:
    """
    用 BeautifulSoup 解析 HTML，返回 [(标题, 绝对链接), ...]。
    HN 每条新闻在 <tr class="athing"> 里，标题在 .titleline > a。
    """
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.select("tr.athing")
    stories: list[tuple[str, str]] = []

    for row in rows:
        if len(stories) >= limit:
            break
        title_a = row.select_one("span.titleline > a")
        if title_a is None or not title_a.get("href"):
            continue
        title = title_a.get_text(strip=True)
        href = title_a["href"].strip()
        full_url = href if href.startswith("http") else urljoin(HN_URL, href)
        stories.append((title, full_url))

    return stories


def translate_to_chinese(text: str, session: requests.Session) -> str:
    """调用 MyMemory 免费接口，把英文译成中文（langpair=en|zh-CN）。"""
    params = {"q": text, "langpair": "en|zh-CN"}
    response = session.get(TRANSLATE_API, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    translated = data.get("responseData", {}).get("translatedText", "")
    if not translated:
        return text
    # 接口有时会把原文原样返回；若明显失败就退回英文
    if "MYMEMORY WARNING" in translated.upper():
        return text
    return translated


def build_markdown(stories: list[tuple[str, str, str]], today: date) -> str:
    """把列表拼成你要的 Markdown 文本。"""
    lines: list[str] = [
        f"# Hacker News 中文摘要 - {today.isoformat()}",
        "",
    ]
    for i, (zh_title, en_title, link) in enumerate(stories, start=1):
        lines.append(f"{i}. [{zh_title}] - [{en_title}]")
        lines.append(f"   链接:{link}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    today = date.today()
    out_dir = Path(__file__).resolve().parent
    out_file = out_dir / f"hn-summary-{today.isoformat()}.md"

    results: list[tuple[str, str, str]] = []
    with requests.Session() as session:
        # trust_env=False：忽略环境变量里的 HTTP(S)_PROXY，避免本机误配代理导致连不上。
        # 若你在公司网络必须走代理，改成 True，并正确配置终端/系统代理。
        session.trust_env = False

        print("正在下载 Hacker News 首页…")
        html = fetch_hn_html(session)

        print("正在解析前 20 条新闻…")
        raw_stories = parse_top_stories(html, TOP_N)
        if len(raw_stories) < TOP_N:
            print(
                f"注意：只解析到 {len(raw_stories)} 条（页面结构可能变化或网络不完整）。"
            )

        for idx, (en_title, link) in enumerate(raw_stories, start=1):
            print(f"翻译第 {idx}/{len(raw_stories)} 条…")
            try:
                zh_title = translate_to_chinese(en_title, session)
            except (requests.RequestException, json.JSONDecodeError) as exc:
                print(f"  翻译失败，保留英文标题。原因可能是网络或 API 限流：{exc}")
                zh_title = en_title
            results.append((zh_title, en_title, link))
            time.sleep(SLEEP_BETWEEN_TRANSLATIONS)

    markdown = build_markdown(results, today)
    out_file.write_text(markdown, encoding="utf-8")
    print(f"已保存：{out_file}")


if __name__ == "__main__":
    main()
