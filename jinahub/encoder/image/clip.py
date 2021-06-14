import clip
import torch
import numpy as np
from jina import Executor, DocumentArray, requests


class CLIPImageEncoder(Executor):
    """Encode image into embeddings."""

    def __init__(self, model_name: str = 'ViT-B/32', device=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not device:
            device = "cuda" if not device and torch.cuda.is_available() else "cpu"
        model, _ = clip.load(model_name, device)
        self.model = model

    @requests
    def encode(self, docs: DocumentArray, **kwargs):
        with torch.no_grad():
            for doc in docs:
                content = np.expand_dims(doc.content, axis=0)
                input = torch.from_numpy(content)
                embed = self.model.encode_image(input)
                doc.embedding = embed.cpu().numpy().flatten()