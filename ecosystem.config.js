module.exports = {
  apps: [
    {
      name: 'runtime-rush-backend',
      cwd: './backend',
      script: 'uvicorn',
      args: 'app.main:app --host 0.0.0.0 --port 8000',
      interpreter: 'python',
      env: {
        PYTHONPATH: '.'
      },
      error_file: './logs/backend-error.log',
      out_file: './logs/backend-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      autorestart: true,
      watch: false,
      max_memory_restart: '1G'
    },
    {
      name: 'runtime-rush-frontend',
      cwd: './frontend',
      script: 'npm',
      args: 'start',
      env: {
        PORT: 3000,
        BROWSER: 'none'
      },
      error_file: './logs/frontend-error.log',
      out_file: './logs/frontend-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      autorestart: true,
      watch: false,
      max_memory_restart: '1G'
    }
  ]
};
