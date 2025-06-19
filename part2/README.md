# 🏗️ Business Logic Layer

The `app/models/` directory defines the core domain entities for HBnB. Each class inherits from a shared **BaseModel** which provides:

- 🔑 **UUID `id`**: globally unique identifier
- 🕒 **Timestamps**: `created_at` & `updated_at`
- 🛠️ **Methods**:
  - 💾 `save()` — update `updated_at`
  - ⚙️ `update(data: dict)` — bulk-update attributes and call `save()`

---

## 🌟 BaseModel

**File:** `app/models/base_model.py`

```python
import uuid
from datetime import datetime

class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now()

    def update(self, data: dict):
        """Bulk-update valid attributes then update timestamp."""
        for key, val in data.items():
            if hasattr(self, key):
                setattr(self, key, val)
        self.save()
