from __future__ import annotations

import os

from fastapi.middleware.cors import CORSMiddleware

from msb_v2.api.web import create_app

app = create_app()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8765)))


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
