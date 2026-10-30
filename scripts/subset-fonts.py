#!/usr/bin/env python3
"""블로그 폰트 파일을 만든다. 레포 루트에서 한 번 실행하면 된다.

본문 Pretendard: 공식 파일이 굵기 하나에 750KB라서 둘로 자른다.
  core  기본 라틴·기호 + KS X 1001 한글 2,350자. 모든 페이지가 받는다.
  rest  나머지 한글 8,822자. 그 글자가 나오는 페이지에서만 받는다.
  Pretendard는 OFL 예약 이름(RFN)이 걸려 있어서, 잘라낸 수정본에는 원래 이름을 쓸 수 없다.
  그래서 폰트 안의 이름을 FAMILY로 바꾼다. 저작권·라이선스 고지는 그대로 남긴다.
제목 SUIT, 코드 IBM Plex Mono: 공식 파일을 손대지 않고 그대로 받는다.
"""
import io
import sys
import urllib.request
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

OUT = Path('src/assets/fonts')
FAMILY = 'Gyuho Sans'
PRETENDARD = 'https://cdn.jsdelivr.net/npm/pretendard@1.3.9/dist/web/static/woff2/Pretendard-{}.woff2'
AS_IS = {
    'head-700.woff2': 'https://cdn.jsdelivr.net/npm/@sun-typeface/suit@2.0.5/fonts/static/woff2/SUIT-Bold.woff2',
    'code-400.woff2': 'https://cdn.jsdelivr.net/npm/@ibm/plex-mono@2.5.0/fonts/split/woff2/IBMPlexMono-Regular-Latin1.woff2',
    'LICENSE-Pretendard.txt': 'https://raw.githubusercontent.com/orioncactus/pretendard/v1.3.9/LICENSE',
    'LICENSE-SUIT.txt': 'https://cdn.jsdelivr.net/npm/@sun-typeface/suit@2.0.5/LICENSE',
    'LICENSE-IBM-Plex.txt': 'https://cdn.jsdelivr.net/npm/@ibm/plex-mono@2.5.0/LICENSE.txt',
}

KS = {ord(bytes([hi, lo]).decode('euc-kr')) for hi in range(0xB0, 0xC9) for lo in range(0xA1, 0xFF)}
BASE = (set(range(0x20, 0x7F)) | set(range(0xA0, 0x100)) | set(range(0x2000, 0x2070))
        | {0x20A9, 0x2116, 0x2122} | set(range(0x2190, 0x2200)) | set(range(0x2460, 0x24FF))
        | set(range(0x3000, 0x3040)) | set(range(0x3131, 0x318F)) | set(range(0xFF01, 0xFF5F)))
PARTS = {'core': BASE | KS, 'rest': set(range(0xAC00, 0xD7A4)) - KS}


def fetch(url: str) -> bytes:
    with urllib.request.urlopen(url) as r:
        return r.read()


def rename(font: TTFont, style: str) -> None:
    ps = f"{FAMILY.replace(' ', '')}-{style}"
    names = {1: FAMILY, 3: f'{ps};subset', 4: f'{FAMILY} {style}', 6: ps, 16: FAMILY, 17: style}
    table = font['name']
    table.names = [r for r in table.names if r.nameID not in names]
    for name_id, value in names.items():
        table.setName(value, name_id, 3, 1, 0x409)
    if 'CFF ' in font:  # CFF 기반 폰트는 이 테이블에도 이름이 따로 있다
        cff = font['CFF '].cff
        cff.fontNames = [ps]
        top = cff.topDictIndex[0]
        top.FullName, top.FamilyName = f'{FAMILY} {style}', FAMILY


def cut(data: bytes, unicodes: set[int], style: str) -> TTFont:
    font = TTFont(io.BytesIO(data))
    opts = subset.Options()
    opts.layout_features = ['*']
    opts.name_IDs = ['*']  # 기본값은 저작권·라이선스 이름 레코드를 지운다
    sub = subset.Subsetter(opts)
    sub.populate(unicodes=unicodes)
    sub.subset(font)
    rename(font, style)
    font.flavor = 'woff2'
    return font


def main() -> None:
    if not Path('astro.config.mjs').exists():
        sys.exit('레포 루트(astro.config.mjs가 있는 곳)에서 실행해.')
    OUT.mkdir(parents=True, exist_ok=True)

    for weight, style in ((400, 'Regular'), (700, 'Bold')):
        data = fetch(PRETENDARD.format(style))
        for part, unicodes in PARTS.items():
            path = OUT / f'body-{weight}.{part}.woff2'
            cut(data, unicodes, style).save(path)
            print(f'{path}  {path.stat().st_size // 1024}KB')

    for name, url in AS_IS.items():
        path = OUT / name
        path.write_bytes(fetch(url))
        print(f'{path}  {path.stat().st_size // 1024}KB')


if __name__ == '__main__':
    main()