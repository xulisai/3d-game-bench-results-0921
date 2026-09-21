import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace buildTower and upgradeTower
old_build_func = """    function buildTower(platform, type) {
      if (gameState.phase !== 'defending') return;
      if (platform.hasTower) return;
      const towerDef = TOWER_SPECS[type];
      if (gameState.gold < towerDef.cost) return;

      gameState.gold -= towerDef.cost;
      gameState.towersBuilt++;

      const lvl = 1;
      const lvlConfig = towerDef.levels[lvl];
      const effectiveRange = platform.onMesa ? lvlConfig.mesaRange : lvlConfig.baseRange;
      const model = createTowerModel(type, platform.onMesa, lvl);
      model.root.position.set(platform.x, platform.y, platform.z);
      scene.add(model.root);

      const tower = {
        platform: platform,
        type: type,
        level: lvl,
        levelConfig: lvlConfig,
        effectiveRange: effectiveRange,
        model: model,
        x: platform.x,
        y: platform.y,
        z: platform.z,
        fireCooldown: 0,
        target: null,
        blockedLoS: false
      };

      // Set interactive click target on tower base/shaft for upgrades
      model.root.traverse(child => {
        if (child.isMesh) {
          child.userData = { isTowerMesh: true, towerObj: tower };
        }
      });

      platform.hasTower = true;
      platform.tower = tower;
      towers.push(tower);

      closeBuildMenu();
      updateHUD();
      updateArenaState();
    }

    function upgradeTower(tower) {
      if (gameState.phase !== 'defending') return;
      if (tower.level >= 3) return;

      const nextLevel = tower.level + 1;
      const upgradePrice = tower.levelConfig.upgradeCost;
      if (gameState.gold < upgradePrice) return;

      gameState.gold -= upgradePrice;

      // Remove old 3D model
      scene.remove(tower.model.root);

      // Create upgraded model
      tower.level = nextLevel;
      tower.levelConfig = TOWER_SPECS[tower.type].levels[nextLevel];
      tower.effectiveRange = tower.platform.onMesa ? tower.levelConfig.mesaRange : tower.levelConfig.baseRange;

      const newModel = createTowerModel(tower.type, tower.platform.onMesa, nextLevel);
      newModel.root.position.set(tower.x, tower.y, tower.z);
      scene.add(newModel);
      tower.model = newModel;

      newModel.root.traverse(child => {
        if (child.isMesh) {
          child.userData = { isTowerMesh: true, towerObj: tower };
        }
      });

      updateUpgradeMenu(tower);
      updateHUD();
      updateArenaState();
    }"""

new_build_func = """    function buildTower(platform, type) {
      if (gameState.phase !== 'defending') return;
      if (platform.hasTower) return;
      const towerDef = TOWER_SPECS[type];
      if (gameState.gold < towerDef.cost) return;

      gameState.gold -= towerDef.cost;
      gameState.towersBuilt++;

      const lvl = 1;
      const lvlConfig = towerDef.levels[lvl];
      const model = createTowerModel(type, platform.onMesa, lvl);
      model.root.position.set(platform.x, platform.y, platform.z);
      scene.add(model.root);

      let effectiveRange = 0;
      if (type === 'barracks') {
        effectiveRange = platform.onMesa ? lvlConfig.mesaRallyRange : lvlConfig.rallyRange;
      } else {
        effectiveRange = platform.onMesa ? lvlConfig.mesaRange : lvlConfig.baseRange;
      }

      const tower = {
        platform: platform,
        type: type,
        level: lvl,
        levelConfig: lvlConfig,
        effectiveRange: effectiveRange,
        model: model,
        x: platform.x,
        y: platform.y,
        z: platform.z,
        fireCooldown: 0,
        target: null,
        blockedLoS: false,
        soldiers: [],
        rallyPoint: null,
        rallyFlag: null
      };

      if (type === 'barracks') {
        // Initialize default rally point on nearest road lane
        const defaultRally = getNearestLanePoint(platform.x, platform.z);
        tower.rallyPoint = defaultRally.clone();

        const flag = createRallyFlagMesh();
        flag.root.position.copy(tower.rallyPoint);
        scene.add(flag.root);
        tower.rallyFlag = flag;

        // Spawn initial soldiers for barracks
        for (let s = 0; s < lvlConfig.maxSoldiers; s++) {
          spawnBarracksSoldier(tower, s);
        }
      }

      // Set interactive click target on tower base/shaft for upgrades
      model.root.traverse(child => {
        if (child.isMesh) {
          child.userData = { isTowerMesh: true, towerObj: tower };
        }
      });

      platform.hasTower = true;
      platform.tower = tower;
      towers.push(tower);

      closeBuildMenu();
      updateHUD();
      updateArenaState();
    }

    function spawnBarracksSoldier(tower, soldierIndex) {
      const lvl = tower.level;
      const cfg = tower.levelConfig;
      const model = createSoldierModel(lvl);

      // Start position: at barracks door
      const startPos = new THREE.Vector3(tower.x, tower.y, tower.z);
      model.root.position.copy(startPos);
      scene.add(model.root);

      const soldier = {
        tower: tower,
        index: soldierIndex,
        level: lvl,
        maxHealth: cfg.soldierHp,
        health: cfg.soldierHp,
        damage: cfg.soldierDmg,
        attackSpeed: cfg.soldierAtkSpeed,
        attackCooldown: 0,
        speed: 3.2,
        model: model,
        pos: startPos.clone(),
        engagedEnemy: null,
        isDead: false,
        respawnTimer: 0,
        walkAnimTime: 0
      };

      tower.soldiers.push(soldier);
      return soldier;
    }

    function upgradeTower(tower) {
      if (gameState.phase !== 'defending') return;
      if (tower.level >= 3) return;

      const nextLevel = tower.level + 1;
      const upgradePrice = tower.levelConfig.upgradeCost;
      if (gameState.gold < upgradePrice) return;

      gameState.gold -= upgradePrice;

      // Remove old 3D model
      scene.remove(tower.model.root);

      // Create upgraded model
      tower.level = nextLevel;
      tower.levelConfig = TOWER_SPECS[tower.type].levels[nextLevel];

      if (tower.type === 'barracks') {
        tower.effectiveRange = tower.platform.onMesa ? tower.levelConfig.mesaRallyRange : tower.levelConfig.rallyRange;
      } else {
        tower.effectiveRange = tower.platform.onMesa ? tower.levelConfig.mesaRange : tower.levelConfig.baseRange;
      }

      const newModel = createTowerModel(tower.type, tower.platform.onMesa, nextLevel);
      newModel.root.position.set(tower.x, tower.y, tower.z);
      scene.add(newModel.root);
      tower.model = newModel;

      newModel.root.traverse(child => {
        if (child.isMesh) {
          child.userData = { isTowerMesh: true, towerObj: tower };
        }
      });

      // If barracks, upgrade existing soldiers or produce extra soldiers if capacity increased
      if (tower.type === 'barracks') {
        const cfg = tower.levelConfig;
        tower.soldiers.forEach(soldier => {
          soldier.level = nextLevel;
          soldier.maxHealth = cfg.soldierHp;
          soldier.health = cfg.soldierHp;
          soldier.damage = cfg.soldierDmg;
          soldier.attackSpeed = cfg.soldierAtkSpeed;

          // Rebuild soldier 3D model with higher level visuals
          const oldPos = soldier.pos.clone();
          const oldRot = soldier.model.root.rotation.clone();
          scene.remove(soldier.model.root);
          const newSolModel = createSoldierModel(nextLevel);
          newSolModel.root.position.copy(oldPos);
          newSolModel.root.rotation.copy(oldRot);
          scene.add(newSolModel.root);
          soldier.model = newSolModel;
        });

        // If maxSoldiers increased (e.g. lvl 3 max is 3)
        while (tower.soldiers.length < cfg.maxSoldiers) {
          spawnBarracksSoldier(tower, tower.soldiers.length);
        }
      }

      updateUpgradeMenu(tower);
      updateHUD();
      updateArenaState();
    }"""

assert old_build_func in text, "old_build_func not found"
text = text.replace(old_build_func, new_build_func, 1)

print("buildTower and upgradeTower updated successfully.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
