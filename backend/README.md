# Finly — Local Development Setup

## Prerequisites
- macOS with Homebrew installed
- Python 3.x
- Node.js (for frontend later)

---

## PostgreSQL Setup

### 1. Install PostgreSQL
```bash
brew install postgresql@18
```

### 2. Add to PATH
```bash
echo 'export PATH="/opt/homebrew/opt/postgresql@18/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### 3. Start PostgreSQL
```bash
brew services start postgresql
```

### 4. Create Database & User
```bash
psql postgres
```
Then inside psql:
```sql
CREATE USER finly_user WITH PASSWORD 'finly123';
CREATE DATABASE finly_db OWNER finly_user;
GRANT ALL PRIVILEGES ON DATABASE finly_db TO finly_user;
\q
```

### 5. Connect to Database
```bash
psql -U finly_user -d finly_db
```

### 6. Stop PostgreSQL (when not needed)
```bash
brew services stop postgresql
```

---

## Project Structure
```
finly/
├── frontend/     # Next.js
├── backend/      # FastAPI (Python)
├── terraform/    # AWS Infrastructure
└── README.md
```

## Database Schema

### Connect to Database
```bash
psql -U finly_user -d finly_db
```

### Create Tables
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE expenses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    amount DECIMAL(10,2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT,
    date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Verify Tables
```bash
\dt
```