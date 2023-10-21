# Data Pulse

Data Pulse is a project designed for efficient data analysis and visualization. It combines a powerful backend with a user-friendly frontend to provide seamless data processing.

## Prerequisites
- Python 3.6+
- Node.js
- npm

## Setup Instructions

### Backend
1. Create Virtual Environment
```bash
make init-backend
```
2. Install Backend Dependencies
```bash
make install-backend
```
### Frontend
1. Install Frontend Dependencies
```bash
make install-frontend
```
2. Build Frontend
```bash
make build-frontend
```

## Running the Application
1. Start Backend Server
```bash
make start-backend
```
2. Start Frontend Server
```bash
make start-frontend
```

## Testing
1. Run Backend Tests
```bash
make test-backend
```
2. Generate Backend Coverage Report
```bash
make coverage-backend
```
3. Run Frontend Tests
```bash
make test-frontend
```

## Additional Commands
Freeze Backend Dependencies
```bash
make freeze
```
Clean Backend
```bash
make clean-backend
```

Clean Frontend
```bash
make clean-frontend
```

Clean Project
```bash
make clean
```

## License
This project is licensed under the ISC License - see the LICENSE.md file for details.