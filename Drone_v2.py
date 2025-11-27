<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Drone Mission Control - Cyberpunk</title>
    <!-- ВАША БИБЛИОТЕКА КАРТ ДОЛЖНА БЫТЬ ПОДКЛЮЧЕНА ЗДЕСЬ -->
    <!-- <link rel="stylesheet" href="путь/к/вашей/карте.css" /> -->
    <style>
        :root {
            --neon-blue: #0ff;
            --neon-purple: #f0f;
            --dark-bg: #0a0a12;
            --darker-bg: #050508;
            --panel-bg: rgba(16, 16, 32, 0.8);
            --text-color: #e0e0ff;
            --accent: #6b46c1;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Courier New', monospace;
        }
        
        body {
            background-color: var(--dark-bg);
            color: var(--text-color);
            overflow: hidden;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(100, 0, 255, 0.1) 0%, transparent 20%),
                radial-gradient(circle at 90% 80%, rgba(0, 255, 255, 0.1) 0%, transparent 20%);
        }
        
        .container {
            display: grid;
            grid-template-columns: 1fr 300px;
            grid-template-rows: auto 1fr;
            height: 100vh;
            gap: 15px;
            padding: 15px;
        }
        
        header {
            grid-column: 1 / -1;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px;
            background: var(--panel-bg);
            border: 1px solid var(--neon-blue);
            border-radius: 8px;
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
            position: relative;
            overflow: hidden;
        }
        
        header::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.1), transparent);
            animation: scan 3s linear infinite;
        }
        
        @keyframes scan {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        .logo {
            font-size: 24px;
            font-weight: bold;
            color: var(--neon-blue);
            text-shadow: 0 0 10px var(--neon-blue);
        }
        
        .status {
            display: flex;
            gap: 20px;
        }
        
        .status-item {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        .status-label {
            font-size: 12px;
            color: #aaa;
        }
        
        .status-value {
            font-size: 14px;
            color: var(--neon-blue);
            text-shadow: 0 0 5px var(--neon-blue);
        }
        
        .map-container {
            background: var(--panel-bg);
            border: 1px solid var(--neon-blue);
            border-radius: 8px;
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.2);
            overflow: hidden;
            position: relative;
        }
        
        #map {
            width: 100%;
            height: 100%;
        }
        
        .controls-panel {
            background: var(--panel-bg);
            border: 1px solid var(--neon-purple);
            border-radius: 8px;
            box-shadow: 0 0 15px rgba(255, 0, 255, 0.2);
            padding: 15px;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        
        .panel-title {
            font-size: 18px;
            color: var(--neon-purple);
            text-shadow: 0 0 5px var(--neon-purple);
            margin-bottom: 10px;
            border-bottom: 1px solid rgba(255, 0, 255, 0.3);
            padding-bottom: 5px;
        }
        
        .mission-controls {
            display: grid;
            grid-template-columns: 1fr;
            gap: 10px;
        }
        
        .control-btn {
            background: var(--darker-bg);
            border: 1px solid;
            border-radius: 4px;
            padding: 12px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s;
            color: var(--text-color);
            position: relative;
            overflow: hidden;
        }
        
        .control-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            transition: left 0.5s;
        }
        
        .control-btn:hover::before {
            left: 100%;
        }
        
            border-left: 3px solid var(--neon-blue);
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(0, 255, 255, 0.4); }
            70% { box-shadow: 0 0 0 5px rgba(0, 255, 255, 0); }
            100% { box-shadow: 0 0 0 0 rgba(0, 255, 255, 0); }
        }
        
        .branch-coords {
            font-size: 12px;
            color: #aaa;
            margin-top: 5px;
        }
        
        .grid-lines {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            background-image: 
                linear-gradient(rgba(0, 255, 255, 0.1) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 255, 255, 0.1) 1px, transparent 1px);
            background-size: 20px 20px;
        }
        
        .pipeline {
            stroke: #0f0;
            stroke-width: 3;
            fill: none;
        }
        
        .branch-marker {
            fill: var(--neon-purple);
            stroke: #fff;
            stroke-width: 1;
            filter: drop-shadow(0 0 5px var(--neon-purple));
        }
        
        .drone-marker {
            fill: var(--neon-blue);
            stroke: #fff;
            stroke-width: 1;
            filter: drop-shadow(0 0 8px var(--neon-blue));
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo">ПОЛЕТЕЛИ</div>
            <div class="status">
                <div class="status-item">
                    <div class="status-label">СТАТУС</div>
                    <div class="status-value" id="status-value">ГОТОВ</div>
                </div>
                <div class="status-item">
                    <div class="status-label">НАЙДЕНО ВРЕЗОК</div>
                    <div class="status-value" id="branches-count">0</div>
                </div>
                <div class="status-item">
                    <div class="status-label">КООРДИНАТЫ</div>
                    <div class="status-value" id="coordinates">55.751244, 37.618423</div>
                </div>
            </div>
        </header>
        
        <div class="map-container">
            <!-- ВСТАВЬТЕ ВАШУ КАРТУ В ЭТОТ КОНТЕЙНЕР -->
            <div id="map">
                <!-- ВАША КАРТА БУДЕТ ЗДЕСЬ -->
                <!-- УДАЛИТЕ ЭТОТ ТЕКСТ И ВСТАВЬТЕ ВАШУ КАРТУ -->
                <div style="width:100%; height:100%; display:flex; justify-content:center; align-items:center; color:#aaa;">
                    тут будет карта сима 
                </div>
            </div>
            <div class="grid-lines"></div>
        </div>
        
        <div class="controls-panel">
            <div class="panel-title">УПРАВЛЕНИЕ МИССИЕЙ</div>
            <div class="mission-controls">
                <button class="control-btn start" id="start-btn">СТАРТ</button>
                <button class="control-btn land" id="land-btn">ПОСАДКА</button>
                <button class="control-btn kill" id="kill-btn">АВАРИЙНОЕ ВЫКЛ.</button>
            </div>
            
            <div class="panel-title">ОБНАРУЖЕННЫЕ ВРЕЗКИ</div>
            <div class="branches-list" id="branches-list">
                <!-- Врезки будут добавляться здесь -->
            </div>
        </div>
    </div>

    <!-- ВАШ СКРИПТ ДЛЯ КАРТЫ ДОЛЖЕН БЫТЬ ПОДКЛЮЧЕН ЗДЕСЬ -->
    <!-- <script src="путь/к/вашей/карте.js"></script> -->
    
    <script>
        // ПЕРЕМЕННЫЕ ДЛЯ ВАШЕЙ КАРТЫ
        // let map; // Ваш объект карты
        
        // ИНИЦИАЛИЗАЦИЯ ВАШЕЙ КАРТЫ
        // function initMap() {
        // map = new YourMapLibrary.Map('map', { ... });
        // // Добавьте вашу карту, слои и другие элементы
        // }
        
        // Переменные состояния
        let missionStarted = false;
        let branchesFound = 0;
        const branchesList = document.getElementById('branches-list');
        const branchesCount = document.getElementById('branches-count');
        const statusValue = document.getElementById('status-value');
        const coordinates = document.getElementById('coordinates');
        const startBtn = document.getElementById('start-btn');
        const landBtn = document.getElementById('land-btn');
        const killBtn = document.getElementById('kill-btn');
        
        // Основная труба нефтепровода (примерные координаты)
        const pipelineCoords = [
            [55.750, 37.615],
            [55.751, 37.617],
            [55.752, 37.619],
            [55.753, 37.621],
            [55.754, 37.623]
        ];
        
        // ФУНКЦИЯ ДЛЯ ОТРИСОВКИ ТРУБЫ НА ВАШЕЙ КАРТЕ
        // function drawPipeline(coords) {
        // // Используйте API вашей карты для отрисовки линии трубы
        // }
        
        // ФУНКЦИЯ ДЛЯ ОБНОВЛЕНИЯ ПОЗИЦИИ ДРОНА НА ВАШЕЙ КАРТЕ
        function updateDronePosition(lat, lng) {
            // Используйте API вашей карты для обновления позиции маркера дрона
            coordinates.textContent = `${lat.toFixed(6)}, ${lng.toFixed(6)}`;
            
            // Если ваша карта поддерживает центрирование:
            // map.setCenter([lat, lng]);
        }
        
        // ФУНКЦИЯ ДЛЯ ДОБАВЛЕНИЯ МАРКЕРА ВРЕЗКИ НА ВАШУ КАРТУ
        function addBranchToMap(lat, lng) {
            // Используйте API вашей карты для добавления маркера врезки
        }
        
        // Функция добавления найденной врезки
        function addBranch(lat, lng) {
            branchesFound++;
            branchesCount.textContent = branchesFound;
            
            // Добавление маркера на карту
            addBranchToMap(lat, lng);
        // ИНИЦИАЛИЗАЦИЯ ВАШЕЙ КАРТЫ ПРИ ЗАГРУЗКЕ
        // window.onload = function() {
        // initMap();
        // drawPipeline(pipelineCoords);
        // };
        
        // Добавление начальных элементов для демонстрации
        setTimeout(() => {
            addBranch(55.7515, 37.6175);
            addBranch(55.7522, 37.6198);
        }, 1000);
    </script>
</body>
</html>  