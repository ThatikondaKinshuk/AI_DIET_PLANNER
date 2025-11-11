# ☁️ Deployment Guide

Deploy your AI Diet Planner to the cloud and make it accessible online!

## Streamlit Cloud Deployment (Recommended)

Streamlit Cloud offers free hosting for Streamlit apps with GitHub integration.

### Prerequisites
- GitHub account
- This repository forked to your account

### Deployment Steps

1. **Sign Up for Streamlit Cloud**
   - Go to [streamlit.io/cloud](https://streamlit.io/cloud)
   - Sign in with your GitHub account

2. **Create New App**
   - Click "New app" button
   - Select your GitHub repository: `AI_DIET_PLANNER`
   - Choose branch: `main` (or your default branch)
   - Set main file path: `app.py`

3. **Configure Settings**
   - Python version: 3.8+
   - Advanced settings (optional):
     - Add custom subdomain
     - Set resource limits

4. **Deploy**
   - Click "Deploy!" button
   - Wait for deployment to complete (2-5 minutes)
   - Your app will be live at: `https://[your-app-name].streamlit.app`

### Database Considerations

The SQLite database (`diet_planner.db`) will work on Streamlit Cloud with these limitations:

- **Persistence**: Data persists during the session but may reset on app restart
- **Multi-user**: All users share the same database
- **Storage**: Limited to app container storage

For production use with persistent data, consider upgrading to a cloud database.

## Alternative: Cloud Database (Production)

For a production deployment with persistent data:

### Option 1: PostgreSQL (Recommended for Production)

1. **Setup PostgreSQL** on a cloud provider:
   - [ElephantSQL](https://www.elephantsql.com/) (Free tier available)
   - [Heroku Postgres](https://www.heroku.com/postgres)
   - [AWS RDS](https://aws.amazon.com/rds/postgresql/)

2. **Update `database.py`**:
   ```python
   # Change from SQLite to PostgreSQL
   DATABASE_URL = os.environ.get('DATABASE_URL')
   engine = create_engine(DATABASE_URL)
   ```

3. **Add to Streamlit secrets**:
   - In Streamlit Cloud dashboard
   - Go to app settings → Secrets
   - Add your database connection string

### Option 2: MySQL

Similar to PostgreSQL:
- [PlanetScale](https://planetscale.com/) (Free tier)
- [AWS RDS MySQL](https://aws.amazon.com/rds/mysql/)

## Heroku Deployment

1. **Create `Procfile`**:
   ```
   web: sh setup.sh && streamlit run app.py
   ```

2. **Create `setup.sh`**:
   ```bash
   mkdir -p ~/.streamlit/
   echo "[server]
   headless = true
   port = $PORT
   enableCORS = false
   " > ~/.streamlit/config.toml
   ```

3. **Deploy**:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

## Docker Deployment

1. **Create `Dockerfile`**:
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   
   EXPOSE 8501
   
   CMD ["streamlit", "run", "app.py"]
   ```

2. **Build and run**:
   ```bash
   docker build -t ai-diet-planner .
   docker run -p 8501:8501 ai-diet-planner
   ```

## Environment Variables

If using cloud databases, set these environment variables:

```bash
DATABASE_URL=postgresql://user:password@host:port/dbname
SECRET_KEY=your-secret-key-here
```

## Security Considerations

For production deployments:

1. **Database Security**
   - Use environment variables for credentials
   - Never commit database credentials to Git
   - Enable SSL/TLS for database connections

2. **Input Validation**
   - Validate all user inputs
   - Sanitize data before database insertion
   - Implement rate limiting if needed

3. **Access Control**
   - Add authentication if needed
   - Implement user sessions
   - Consider adding admin roles

## Monitoring & Maintenance

- **Logs**: Check Streamlit Cloud logs for errors
- **Updates**: Update dependencies regularly
- **Backups**: Backup database regularly if using cloud DB
- **Performance**: Monitor app performance and resource usage

## Cost Estimation

### Free Tier (Streamlit Cloud)
- Perfect for personal use or demos
- 1GB storage, limited compute
- Community support

### Production Setup
- Streamlit Cloud: Free - $250/month
- Database (PostgreSQL): Free - $50/month
- Total: $0 - $300/month depending on usage

## Post-Deployment Checklist

- [ ] App is accessible via URL
- [ ] All features work correctly
- [ ] Database is storing data
- [ ] Export/download features work
- [ ] Mobile responsive design works
- [ ] Error handling is working
- [ ] Custom domain configured (optional)

## Getting Help

- Streamlit Documentation: [docs.streamlit.io](https://docs.streamlit.io)
- Streamlit Forum: [discuss.streamlit.io](https://discuss.streamlit.io)
- GitHub Issues: Report bugs in your repository

## Next Steps After Deployment

1. Share your app URL with users
2. Gather feedback
3. Monitor usage and performance
4. Plan for scaling if needed
5. Add new features based on user requests

---

**Happy Deploying! 🚀**

Your AI Diet Planner will help users worldwide achieve their health goals!
