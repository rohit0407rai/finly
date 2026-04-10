# Base image — Python 3.13 slim version
# slim = chhota size, sirf zaruri cheezein
FROM python:3.13-slim

# Working directory set karo container ke andar
# ye folder automatically ban jayega
WORKDIR /app

# Pehle sirf requirements copy karo
# (code nahi — ye caching ke liye hai)
COPY requirements.txt .

# Dependencies install karo
RUN pip install --no-cache-dir -r requirements.txt

# Ab baaki code copy karo
COPY . .

# Port expose karo
# (sirf documentation ke liye — actual port mapping docker run me hoti hai)
EXPOSE 8000

# App start karo
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]