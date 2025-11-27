<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Drone Mission Control - Cyberpunk</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
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
        
        .control-btn.start {
            border-color: #0f0;
            box-shadow: 0 0 10px rgba(0, 255, 0, 0.3);
        }
        
        .control-btn.start:hover {
            background: rgba(0, 255, 0, 0.1);
            box-shadow: 0 0 15px rgba(0, 255, 0, 0.5);
        }
        
        .control-btn.land {
            border-color: #ff0;
            box-shadow: 0 0 10px rgba(255, 255, 0, 0.3);
        }
        
        .control-btn.land:hover {
            background: rgba(255, 255, 0, 0.1);
            box-shadow: 0 0 15px rgba(255, 255, 0, 0.5);
        }
        
        .control-btn.kill {
            border-color: #f00;
            box-shadow: 0 0 10px rgba(255, 0, 0, 0.3);
        }
        
        .control-btn.kill:hover {
            background: rgba(255, 0, 0, 0.1);
            box-shadow: 0 0 15px rgba(255, 0, 0, 0.5);
        }
        
        .control-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .control-btn:disabled:hover {
            background: var(--darker-bg);
            box-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
        }
        
        .branches-list {
            flex-grow: 1;
            overflow-y: auto;
            background: var(--darker-bg);
            border-radius: 4px;
            padding: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .branch-item {
            padding: 10px;
            margin-bottom: 8px;
            background: rgba(30, 30, 60, 0.5);
            border-radius: 4px;
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
            <div class="logo">DRONE MISSION CONTROL v2.1.7</div>
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
            <div id="map"></div>
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

    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <script>
        // Инициализация карты
        const map = L.map('map').setView([55.751244, 37.618423], 15);
        
        // Добавление слоя карты (в реальном приложении здесь будет агисо_map)
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);
        
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
        
        // Отрисовка основной трубы
        const pipeline = L.polyline(pipelineCoords, {
            color: '#0f0',
            weight: 4,
            opacity: 0.8
        }).addTo(map);
        
        // Маркер дрона
        const droneMarker = L.circleMarker([55.751244, 37.618423], {
            color: '#0ff',
            fillColor: '#0ff',
            fillOpacity: 0.7,
            radius: 8
        }).addTo(map);
        
        // Функция обновления координат дрона
        function updateDronePosition(lat, lng) {
            droneMarker.setLatLng([lat, lng]);
            coordinates.textContent = `${lat.toFixed(6)}, ${lng.toFixed(6)}`;
            map.panTo([lat, lng]);
        }
        
        // Функция добавления найденной врезки
        function addBranch(lat, lng) {
            branchesFound++;
            branchesCount.textContent = branchesFound;
            
            // Добавление маркера на карту
            L.circleMarker([lat, lng], {
                color: '#f0f',
                fillColor: '#f0f',
                fillOpacity: 0.7,
                radius: 6
            }).addTo(map);
            
            // Добавление в список
            const branchItem = document.createElement('div');
            branchItem.className = 'branch-item';
            branchItem.innerHTML = `
                <div>Врезка #${branchesFound}</div>
                <div class="branch-coords">${lat.toFixed(6)}, ${lng.toFixed(6)}</div>
            `;
            branchesList.appendChild(branchItem);
            
            // Прокрутка списка к последнему элементу
            branchesList.scrollTop = branchesList.scrollHeight;
        }
        
        // Обработчики кнопок
        startBtn.addEventListener('click', function() {
            if (!missionStarted) {
                missionStarted = true;
                statusValue.textContent = 'МИССИЯ ВЫПОЛНЯЕТСЯ';
                startBtn.disabled = true;
                
                // Имитация полета дрона и обнаружения врезок
                simulateMission();
            }
        });
        
        landBtn.addEventListener('click', function() {
            if (missionStarted) {
                missionStarted = false;
                statusValue.textContent = 'ПОСАДКА ВЫПОЛНЕНА';
                startBtn.disabled = false;
            }
        });
        
        killBtn.addEventListener('click', function() {
            missionStarted = false;
            statusValue.textContent = 'АВАРИЙНОЕ ОТКЛЮЧЕНИЕ';
            startBtn.disabled = false;
        });
        
        // Функция имитации миссии
        function simulateMission() {
            if (!missionStarted) return;
            
            let progress = 0;
            const interval = setInterval(() => {
                if (!missionStarted) {
                    clearInterval(interval);
                    return;
                }
                
                progress += 0.01;
                
                // Обновление позиции дрона вдоль трубы
                const pipelineIndex = Math.floor(progress * (pipelineCoords.length - 1));
                if (pipelineIndex < pipelineCoords.length - 1) {
                    const startCoord = pipelineCoords[pipelineIndex];
                    const endCoord = pipelineCoords[pipelineIndex + 1];
                    const segmentProgress = (progress * (pipelineCoords.length - 1)) - pipelineIndex;
                    
                    const lat = startCoord[0] + (endCoord[0] - startCoord[0]) * segmentProgress;
                    const lng = startCoord[1] + (endCoord[1] - startCoord[1]) * segmentProgress;
                    
                    updateDronePosition(lat, lng);
                    
                    // Случайное обнаружение врезки
                    if (Math.random() < 0.05 && progress < 0.95) {
                        // Врезка находится рядом с основной трубой
                        const branchLat = lat + (Math.random() - 0.5) * 0.002;
                        const branchLng = lng + (Math.random() - 0.5) * 0.002;
                        addBranch(branchLat, branchLng);
                    }
                } else {
                    // Миссия завершена
                    missionStarted = false;
                    statusValue.textContent = 'МИССИЯ ЗАВЕРШЕНА';
                    startBtn.disabled = false;
                    clearInterval(interval);
                }
            }, 100);
        }
        
        // Добавление начальных элементов для демонстрации
        setTimeout(() => {
            addBranch(55.7515, 37.6175);
            addBranch(55.7522, 37.6198);
        }, 1000);
    </script>
</body>
</html>