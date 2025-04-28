# 🌸 Iris Project

This repository contains an analysis project of the Iris dataset using Docker and Python.

## 📋 Requirements

- [Docker](https://www.docker.com/get-started) - Container platform
- [Docker Compose](https://docs.docker.com/compose/install/) - Multi-container orchestration

## 🚀 Getting Started

### 📥 Clone the Repository

```bash
git clone https://github.com/ediadiaf/iris_project.git
cd iris_project
```

### 🏗️ Build and Run with Docker Compose

To build and start the application:

```bash
docker compose up --build
```

**This command will:**
1. Build the Docker image(s)
2. Create and start container(s)
3. Display container output

🌐 Access the application at [http://localhost:8501](http://localhost:8501)

### 🛑 Stop the Application

- Press `Ctrl+C` in the terminal, or
- Run `docker compose down`

### 🔄 Running in Background

```bash
docker compose up --build -d
docker compose logs -f  # View logs
```

## 📁 Project Structure

```
iris_project/
├── data/               # Dataset files
├── src/                # Source code
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose configuration
└── README.md          # Documentation
```

## ⚙️ Configuration

Configure environment variables in `docker-compose.yml`

## 👩‍💻 Development

1. Fork repository
2. Create feature branch
3. Submit pull request

## 🔧 Troubleshooting

- Port 8501 conflict? Modify port in `docker-compose.yml`
- Database issues? Check environment variables

## 📄 License

GNU License

