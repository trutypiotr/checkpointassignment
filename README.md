# Check Point assignment

### Run services
1. Create `.env` based on `.env_template` and update variables (`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` in elasticmq can be set to anything)
2. Build images and run containers:
   ```
    docker-compose up --build -d
   ```
3. Create superuser
    ```
    docker-compose exec web poetry run python manage.py createsuperuser
    ```

### Slack configuration
1. To receive events locally from slack, configure tunneling with `ngrok`
    ```
   ngrok http http://localhost:8000 
   ```
2. Add ngrok address to `ALLOWED_HOSTS`. Example:
    ```
    ALLOWED_HOSTS=https://1c40-94-40-165-45.ngrok-free.app
   ```
3. Set `{your_ngrok_url}/slack/webhook/` as url in Slack Event Subscriptions
4. Subscribe to bot events: `message.channels`, `message.groups`, `message.im`
5. Add User Token Scopes `chat:write`
6. Set Slack variables in `.env`

### Testing

#### Django
```
docker-compose exec web poetry run python manage.py test
```
#### DLP
```
docker-compose exec dlp poetry run python -m unittest discover -s tests
```
