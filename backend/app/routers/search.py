from fastapi import APIRouter
from ..chroma_client import collection

router = APIRouter(prefix='/search')

@router.get('/', summary='検索結果を返す')
async def search(q: str):
    # Chroma から生データ取得
    raw = collection.query(query_texts=[q], n_results=5)
    # raw['candidates'] が文字化けしている場合に復元
    fixed = []
    for text in raw.get('candidates', []):
        if isinstance(text, str):
            try:
                # Latin-1 でエンコード  UTF-8 でデコード
                fixed.append(text.encode('latin1').decode('utf8'))
            except Exception:
                fixed.append(text)
        else:
            fixed.append(text)
    return {'candidates': fixed}
