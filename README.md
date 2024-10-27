# Создание приватного ключа RSA
```shell
openssl genrsa -out jwt-private.pem 2048
```

# Создание публичного ключа из приватного
```shell
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```