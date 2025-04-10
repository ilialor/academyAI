@echo off
setlocal

set PROJECT_ROOT=AcademyOpenAI

echo Creating project structure for %PROJECT_ROOT%...

if exist "%PROJECT_ROOT%" (
    echo Directory %PROJECT_ROOT% already exists. Please remove it or choose a different location.
    exit /b 1
)

mkdir "%PROJECT_ROOT%"
cd "%PROJECT_ROOT%"

REM --- Root Files ---
echo Creating root files...
type nul > .gitignore
type nul > LICENSE
type nul > README.md
type nul > ruff.toml

REM --- GitHub Workflows ---
echo Creating .github directory...
mkdir .github\workflows
type nul > .github\workflows\ci.yml

REM --- Backend ---
echo Creating backend directories...
mkdir backend\auth_service\app\api\v1\endpoints
mkdir backend\auth_service\app\core
mkdir backend\auth_service\app\db
mkdir backend\auth_service\app\schemas
mkdir backend\auth_service\app\services
mkdir backend\auth_service\app\utils
mkdir backend\auth_service\migrations\versions
mkdir backend\auth_service\tests

mkdir backend\courses_service\app\api\v1\endpoints
mkdir backend\courses_service\app\core
mkdir backend\courses_service\app\db
mkdir backend\courses_service\app\schemas
mkdir backend\courses_service\app\services
mkdir backend\courses_service\app\tasks
mkdir backend\courses_service\tests

mkdir backend\pipeline_worker\app\core
mkdir backend\pipeline_worker\app\processors
mkdir backend\pipeline_worker\app\services
mkdir backend\pipeline_worker\app\tasks
mkdir backend\pipeline_worker\app\utils
mkdir backend\pipeline_worker\tests

echo Creating backend files...
REM Auth Service Files
type nul > backend\auth_service\app\api\v1\endpoints\auth.py
type nul > backend\auth_service\app\api\v1\endpoints\users.py
type nul > backend\auth_service\app\api\v1\__init__.py
type nul > backend\auth_service\app\core\config.py
type nul > backend\auth_service\app\db\models.py
type nul > backend\auth_service\app\db\session.py
type nul > backend\auth_service\app\db\__init__.py
type nul > backend\auth_service\app\schemas\token.py
type nul > backend\auth_service\app\schemas\user.py
type nul > backend\auth_service\app\schemas\__init__.py
type nul > backend\auth_service\app\services\auth_service.py
type nul > backend\auth_service\app\services\user_service.py
type nul > backend\auth_service\app\services\__init__.py
type nul > backend\auth_service\app\utils\security.py
type nul > backend\auth_service\app\main.py
type nul > backend\auth_service\app\__init__.py
type nul > backend\auth_service\migrations\env.py
type nul > backend\auth_service\migrations\script.py.mako
type nul > backend\auth_service\tests\test_auth.py
type nul > backend\auth_service\tests\test_users.py
type nul > backend\auth_service\Dockerfile
type nul > backend\auth_service\pyproject.toml
type nul > backend\auth_service\README.md

REM Courses Service Files
type nul > backend\courses_service\app\api\v1\endpoints\courses.py
type nul > backend\courses_service\app\api\v1\__init__.py
type nul > backend\courses_service\app\core\config.py
type nul > backend\courses_service\app\db\models.py
type nul > backend\courses_service\app\db\session.py
type nul > backend\courses_service\app\db\__init__.py
type nul > backend\courses_service\app\schemas\course.py
type nul > backend\courses_service\app\schemas\__init__.py
type nul > backend\courses_service\app\services\course_service.py
type nul > backend\courses_service\app\services\pipeline_service.py
type nul > backend\courses_service\app\services\__init__.py
type nul > backend\courses_service\app\tasks\course_tasks.py
type nul > backend\courses_service\app\main.py
type nul > backend\courses_service\app\__init__.py
type nul > backend\courses_service\tests\test_courses.py
type nul > backend\courses_service\Dockerfile
type nul > backend\courses_service\pyproject.toml
type nul > backend\courses_service\README.md

REM Pipeline Worker Files
type nul > backend\pipeline_worker\app\core\config.py
type nul > backend\pipeline_worker\app\processors\video_processor.py
type nul > backend\pipeline_worker\app\processors\text_processor.py
type nul > backend\pipeline_worker\app\processors\course_generator.py
type nul > backend\pipeline_worker\app\services\ffmpeg_service.py
type nul > backend\pipeline_worker\app\services\llm_service.py
type nul > backend\pipeline_worker\app\services\stt_service.py
type nul > backend\pipeline_worker\app\services\translation_service.py
type nul > backend\pipeline_worker\app\tasks\process_content.py
type nul > backend\pipeline_worker\app\utils\file_handler.py
type nul > backend\pipeline_worker\app\main.py
type nul > backend\pipeline_worker\app\__init__.py
type nul > backend\pipeline_worker\tests\test_processors.py
type nul > backend\pipeline_worker\Dockerfile
type nul > backend\pipeline_worker\pyproject.toml
type nul > backend\pipeline_worker\README.md

REM --- Docs ---
echo Creating docs directories...
mkdir docs\api_specs
echo Creating docs files...
type nul > docs\architecture.md
type nul > docs\api_specs\auth_v1.yaml
type nul > docs\api_specs\courses_v1.yaml

REM --- Frontend ---
echo Creating frontend directories...
mkdir frontend\web_react\public
mkdir frontend\web_react\src\assets
mkdir frontend\web_react\src\components
mkdir frontend\web_react\src\hooks
mkdir frontend\web_react\src\layouts
mkdir frontend\web_react\src\pages
mkdir frontend\web_react\src\services
mkdir frontend\web_react\src\store
mkdir frontend\web_react\src\styles
mkdir frontend\web_react\src\types
mkdir frontend\web_react\src\utils

mkdir frontend\mobile_react_native\android
mkdir frontend\mobile_react_native\ios
mkdir frontend\mobile_react_native\src\assets
mkdir frontend\mobile_react_native\src\components
mkdir frontend\mobile_react_native\src\hooks
mkdir frontend\mobile_react_native\src\navigation
mkdir frontend\mobile_react_native\src\screens
mkdir frontend\mobile_react_native\src\services
mkdir frontend\mobile_react_native\src\store
mkdir frontend\mobile_react_native\src\styles
mkdir frontend\mobile_react_native\src\types
mkdir frontend\mobile_react_native\src\utils

echo Creating frontend files...
REM Web React Files
type nul > frontend\web_react\public\index.html
type nul > frontend\web_react\src\services\auth.ts
type nul > frontend\web_react\src\services\courses.ts
type nul > frontend\web_react\src\App.tsx
type nul > frontend\web_react\src\main.tsx
type nul > frontend\web_react\Dockerfile
type nul > frontend\web_react\package.json
type nul > frontend\web_react\tsconfig.json
type nul > frontend\web_react\vite.config.ts
type nul > frontend\web_react\README.md

REM Mobile React Native Files
type nul > frontend\mobile_react_native\src\App.tsx
type nul > frontend\mobile_react_native\app.json
type nul > frontend\mobile_react_native\index.js
type nul > frontend\mobile_react_native\package.json
type nul > frontend\mobile_react_native\tsconfig.json
type nul > frontend\mobile_react_native\metro.config.js
type nul > frontend\mobile_react_native\README.md

REM --- Infrastructure ---
echo Creating infra directories...
mkdir infra\docker
mkdir infra\kong
mkdir infra\kubernetes\base
mkdir infra\kubernetes\overlays\development
mkdir infra\kubernetes\overlays\production
mkdir infra\kubernetes\charts\auth-service
mkdir infra\kubernetes\charts\courses-service

echo Creating infra files...
type nul > infra\docker\docker-compose.yml
type nul > infra\docker\docker-compose.prod.yml
type nul > infra\docker\.env.example
type nul > infra\kong\kong.yaml

REM --- Scripts ---
echo Creating scripts directory...
mkdir scripts
echo Creating scripts files...
type nul > scripts\create_structure.bat
type nul > scripts\run_local.sh


echo.
echo Structure for %PROJECT_ROOT% created successfully!

endlocal