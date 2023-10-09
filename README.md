# Django Media Site

This Django project is designed to manage and serve TV shows and movies.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Valijonzoda/media-site.git
   cd media-site
   
- Set up a virtual environment and activate it:
  ```bash
  python -m venv venv
  source venv/bin/activate   # On Windows, use: venv\Scripts\activate

Install the required dependencies:
```bash
pip install -r requirements.txt
```
Apply migrations and start the server:

```bash
python manage.py migrate
python manage.py runserver
```
## Usage

- Access the admin interface at: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- API endpoints for shows and movies:
  - Get shows: [http://127.0.0.1:8000/api/shows/](http://127.0.0.1:8000/api/shows/)
  - Get a specific show: [http://127.0.0.1:8000/api/shows/{show_id}/](http://127.0.0.1:8000/api/shows/{show_id}/)
  - Get show seasons: [http://127.0.0.1:8000/api/shows/{show_id}/seasons/](http://127.0.0.1:8000/api/shows/{show_id}/seasons/)
  - Get show episodes: [http://127.0.0.1:8000/api/shows/{show_id}/episodes/](http://127.0.0.1:8000/api/shows/{show_id}/episodes/)
  - Get episode sources: [http://127.0.0.1:8000/api/episodes/{episode_id}/sources/](http://127.0.0.1:8000/api/episodes/{episode_id}/sources/)


To run the project using Docker, follow the Dockerfile and instructions in the repository.

