// ==========================================================================
// FINAL MASTER 3D BIRTHDAY CARD - Realistic Physical 3D Greeting Card Engine
// Three.js + GSAP + Real 3D Card Posture Physics + Romantic Audio Player
// ==========================================================================

(() => {
  'use strict';

  // --- Configuration & Constants ---
  const CARD_W = 5.0;            // Center panel width
  const FLAP_W = CARD_W / 2;     // Each flap width = 2.5
  const CARD_H = 7.0;            // Card height
  const CARD_THICK = 0.048;      // Realistic physical cardstock thickness
  const HALF_THICK = CARD_THICK / 2;

  // Camera viewpoints for natural inspection
  const VIEWS = {
    // Lifted / Standing Upright Views (Natural 3D Greeting Card on Desk / Mantelpiece)
    uprightPerspective: { pos: { x: 3.8, y: 4.8, z: 8.8 }, target: { x: 0.0, y: 3.5, z: 0.0 } },
    uprightFront:       { pos: { x: 0.0, y: 3.5, z: 9.6 }, target: { x: 0.0, y: 3.5, z: 0.0 } },
    openedCenter:       { pos: { x: 0.0, y: 3.6, z: 8.4 }, target: { x: 0.0, y: 3.5, z: 0.0 } },
    openedHeart:        { pos: { x: 0.0, y: 3.4, z: 3.9 }, target: { x: 0.0, y: 3.4, z: 0.0 } },
    openedLeft:         { pos: { x: -2.6, y: 3.5, z: 4.2 }, target: { x: -2.5, y: 3.5, z: 0.6 } },
    openedRight:        { pos: { x: 2.6, y: 3.5, z: 4.2 }, target: { x: 2.5, y: 3.5, z: 0.6 } },
    
    // Flat on Table Views ("Sleeping" on the desk surface)
    tableOverview:      { pos: { x: 0.0, y: 8.5, z: 4.5 }, target: { x: 0.0, y: 0.0, z: 0.0 } },
    closedFront:        { pos: { x: 0.0, y: 3.5, z: 9.6 }, target: { x: 0.0, y: 3.5, z: 0.0 } }
  };

  // State Variables
  let scene, camera, renderer, controls;
  let cardGroup, centerBoard, leftHinge, rightHinge;
  let candleLight, sparkleParticles;
  let shadowMesh;

  let isOpen = false;           // Initially CLOSED as requested by user!
  let isLifted = true;          // Default: Standing Upright in real 3D!
  let isAnimating = false;
  let isMusicPlaying = false;

  let currentTiltDeg = 82;      // 82° upright tilt (tilted back 8° like a real standing card)
  let currentFoldDeg = 152;     // 152° open angle (subtle forward 3D wing curve, not dead flat)

  // Luxury Asset Loading Manager
  const loadingManager = new THREE.LoadingManager();
  const textureLoader = new THREE.TextureLoader(loadingManager);

  let isLoaded = false;
  function finishLoading() {
    if (isLoaded) return;
    isLoaded = true;

    const fillEl = document.getElementById('loadingBarFill');
    const textEl = document.getElementById('loadingPercent');
    if (fillEl) fillEl.style.width = '100%';
    if (textEl) textEl.textContent = '100%';

    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
      setTimeout(() => {
        overlay.classList.add('fade-out');
        setTimeout(() => {
          overlay.style.display = 'none';
        }, 500);
      }, 150);
    }
  }

  loadingManager.onProgress = function(url, itemsLoaded, itemsTotal) {
    const pct = Math.round((itemsLoaded / itemsTotal) * 100);
    const fillEl = document.getElementById('loadingBarFill');
    const textEl = document.getElementById('loadingPercent');
    if (fillEl) fillEl.style.width = pct + '%';
    if (textEl) textEl.textContent = pct + '%';
  };

  loadingManager.onLoad = function() {
    finishLoading();
  };

  // Fast-load safety guarantee: Ensure preloader NEVER stays for more than 4 seconds
  setTimeout(finishLoading, 4000);

  // Audio Elements
  let cardAudio;
  let volumeSlider;

  // =========================================================================
  // INITIALIZATION
  // =========================================================================
  function init() {
    const container = document.getElementById('webgl-container');
    const width = container.clientWidth || window.innerWidth;
    const height = container.clientHeight || window.innerHeight;

    // 1. Romantic Dark Midnight Scene
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x070609);
    scene.fog = new THREE.FogExp2(0x070609, 0.02);

    // 2. Camera looking naturally at the upright standing 3D card (closed front view)
    camera = new THREE.PerspectiveCamera(40, width / height, 0.05, 100);
    camera.position.set(VIEWS.uprightPerspective.pos.x, VIEWS.uprightPerspective.pos.y, VIEWS.uprightPerspective.pos.z);

    // 3. Renderer with Linear Tone Mapping for 100% True-Color Reproduction
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false, powerPreference: 'high-performance' });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.LinearToneMapping;
    renderer.toneMappingExposure = 1.0;
    container.appendChild(renderer.domElement);

    // 4. Smooth, Unconstrained OrbitControls (Custom Cursor-Centered Zoom)
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.07;
    controls.enableZoom = false;          // Custom cursor-centered zoom handles wheel
    controls.enableRotate = true;
    controls.enablePan = true;
    controls.screenSpacePanning = true;
    controls.minPolarAngle = 0.05;        // Full vertical orbit
    controls.maxPolarAngle = Math.PI - 0.05;
    controls.minAzimuthAngle = -Infinity; // Infinite horizontal 360° orbit
    controls.maxAzimuthAngle = Infinity;
    controls.target.set(VIEWS.openedCenter.target.x, VIEWS.openedCenter.target.y, VIEWS.openedCenter.target.z);

    // 5. Studio Lighting
    setupLighting();

    // 6. Ground Studio Table Plinth
    setupTable();

    // 7. Floating Golden Fairy Dust Sparkles
    setupFairySparkles();

    // 8. Build Physical 3D Greeting Card
    buildCard();

    // 9. Setup Audio & Event Listeners
    setupAudio();
    setupEvents();

    // Responsive initial camera calibration for mobile portrait screens
    onWindowResize();

    // 10. Start Animation Loop
    animate();

    // Set initial UI states
    updateLiftUI();
    updateUI();
  }

  // =========================================================================
  // STUDIO LIGHTING
  // =========================================================================
  function setupLighting() {
    // Pure, even ambient light to ensure original photo colors and skin tones are completely preserved
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.96);
    scene.add(ambientLight);

    // Main directional studio key light
    const dirLight = new THREE.DirectionalLight(0xfff8ee, 0.28);
    dirLight.position.set(5.0, 11.0, 6.0);
    dirLight.castShadow = true;
    dirLight.shadow.mapSize.width = 2048;
    dirLight.shadow.mapSize.height = 2048;
    dirLight.shadow.camera.near = 1.0;
    dirLight.shadow.camera.far = 30.0;
    dirLight.shadow.bias = -0.0001;
    dirLight.shadow.radius = 2.5;
    scene.add(dirLight);

    // Soft warm backlight accent to highlight physical cardstock edges
    const backRim = new THREE.DirectionalLight(0xf2e0ff, 0.20);
    backRim.position.set(-5.0, 7.0, -6.0);
    scene.add(backRim);

    // Warm candlelight accent
    candleLight = new THREE.PointLight(0xffa055, 0.40, 16, 2.0);
    candleLight.position.set(0.0, 4.0, 3.0);
    scene.add(candleLight);
  }

  // =========================================================================
  // GROUND STUDIO TABLE PLINTH
  // =========================================================================
  function setupTable() {
    const tableGeo = new THREE.BoxGeometry(22, 0.4, 16);
    const tableMat = new THREE.MeshStandardMaterial({
      color: 0x09080c,
      roughness: 0.88,
      metalness: 0.1
    });
    const table = new THREE.Mesh(tableGeo, tableMat);
    table.position.y = -0.20;
    table.receiveShadow = true;
    scene.add(table);

    // Soft Contact Shadow Plane beneath the card
    const shadowGeo = new THREE.PlaneGeometry(16, 12);
    const shadowMat = new THREE.ShadowMaterial({ opacity: 0.65 });
    shadowMesh = new THREE.Mesh(shadowGeo, shadowMat);
    shadowMesh.rotation.x = -Math.PI / 2;
    shadowMesh.position.y = 0.002;
    shadowMesh.receiveShadow = true;
    scene.add(shadowMesh);
  }

  // =========================================================================
  // FLOATING FAIRY DUST PARTICLES
  // =========================================================================
  function setupFairySparkles() {
    const particleCount = 75;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);

    for (let i = 0; i < particleCount; i++) {
      positions[i * 3]     = (Math.random() - 0.5) * 16.0;
      positions[i * 3 + 1] = Math.random() * 7.5 + 0.2;
      positions[i * 3 + 2] = (Math.random() - 0.5) * 14.0;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

    const pMat = new THREE.PointsMaterial({
      color: 0xffe2a8,
      size: 0.08,
      transparent: true,
      opacity: 0.75,
      blending: THREE.AdditiveBlending
    });

    sparkleParticles = new THREE.Points(geometry, pMat);
    scene.add(sparkleParticles);
  }

  // =========================================================================
  // BUILD PHYSICAL 3D GREETING CARD
  // =========================================================================
  function buildCard() {
    cardGroup = new THREE.Group();
    
    // Initial Posture: Standing Upright in real 3D!
    applyCardPosture(currentTiltDeg, false);
    scene.add(cardGroup);

    // Automatic WebP detection for ultra-fast 749KB loading on mobile (or optimized progressive JPG fallback)
    const canUseWebP = (() => {
      try {
        const elem = document.createElement('canvas');
        if (elem.getContext && elem.getContext('2d')) {
          return elem.toDataURL('image/webp').indexOf('data:image/webp') === 0;
        }
      } catch (e) {}
      return false;
    })();
    const texExt = canUseWebP ? '.webp' : '.jpg';

    function loadCardTexture(name) {
      const tex = textureLoader.load(`textures_3d/${name}${texExt}`);
      tex.generateMipmaps = true;
      tex.minFilter = THREE.LinearMipmapLinearFilter;
      tex.magFilter = THREE.LinearFilter;
      tex.anisotropy = Math.min(renderer.capabilities.getMaxAnisotropy(), 4);
      return tex;
    }

    const texFrontLeft   = loadCardTexture('card_front_left');
    const texFrontRight  = loadCardTexture('card_front_right');
    const texInsideCtr   = loadCardTexture('card_inside_center');
    const texInsideLeft  = loadCardTexture('card_inside_left');
    const texInsideRight = loadCardTexture('card_inside_right');
    const texCardBack    = loadCardTexture('card_back');

    // Premium Cardstock Edge Material (warm ivory paper core)
    const paperEdgeMat = new THREE.MeshStandardMaterial({
      color: 0xf5f1e8,
      roughness: 0.95,
      metalness: 0.0
    });

    const cardBackMat = new THREE.MeshStandardMaterial({
      map: texCardBack,
      roughness: 0.95,
      metalness: 0.0
    });

    function makeCardFaceMat(texture) {
      return new THREE.MeshStandardMaterial({
        map: texture,
        roughness: 1.0,
        metalness: 0.0
      });
    }

    // 1. CENTER BASE BOARD
    const centerBoardGroup = new THREE.Group();
    centerBoardGroup.name = "centerBoardGroup";

    const centerBoxGeo = new THREE.BoxGeometry(CARD_W, CARD_H, CARD_THICK);
    const centerBox = new THREE.Mesh(centerBoxGeo, paperEdgeMat);
    centerBox.castShadow = true;
    centerBox.receiveShadow = true;
    centerBoardGroup.add(centerBox);

    const centerInsideGeo = new THREE.PlaneGeometry(CARD_W, CARD_H);
    const centerInsideMat = makeCardFaceMat(texInsideCtr);
    const centerInsideMesh = new THREE.Mesh(centerInsideGeo, centerInsideMat);
    centerInsideMesh.name = "panelCenter";
    centerInsideMesh.position.z = HALF_THICK + 0.001;
    centerInsideMesh.receiveShadow = true;
    centerBoardGroup.add(centerInsideMesh);

    const centerBackGeo = new THREE.PlaneGeometry(CARD_W, CARD_H);
    const centerBackMesh = new THREE.Mesh(centerBackGeo, cardBackMat);
    centerBackMesh.rotation.y = Math.PI;
    centerBackMesh.position.z = -(HALF_THICK + 0.001);
    centerBackMesh.castShadow = true;
    centerBoardGroup.add(centerBackMesh);

    cardGroup.add(centerBoardGroup);
    centerBoard = centerBoardGroup;

    // 2. LEFT FLAP (Hinged at x = -2.5)
    leftHinge = new THREE.Group();
    leftHinge.name = "leftHinge";
    leftHinge.position.set(-CARD_W / 2, 0, HALF_THICK);

    const leftFlapGroup = new THREE.Group();
    leftFlapGroup.position.set(FLAP_W / 2, 0, 0);

    const flapGeo = new THREE.BoxGeometry(FLAP_W, CARD_H, CARD_THICK);
    const leftBox = new THREE.Mesh(flapGeo, paperEdgeMat);
    leftBox.castShadow = true;
    leftBox.receiveShadow = true;
    leftFlapGroup.add(leftBox);

    // Front Exterior Face (Visible when CLOSED)
    const leftFrontGeo = new THREE.PlaneGeometry(FLAP_W, CARD_H);
    const leftFrontMat = makeCardFaceMat(texFrontLeft);
    const leftFrontMesh = new THREE.Mesh(leftFrontGeo, leftFrontMat);
    leftFrontMesh.name = "frontLeft";
    leftFrontMesh.position.z = HALF_THICK + 0.001;
    leftFrontMesh.castShadow = true;
    leftFrontMesh.receiveShadow = true;
    leftFlapGroup.add(leftFrontMesh);

    // Inside Interior Face (Visible when OPENED)
    const leftInsideGeo = new THREE.PlaneGeometry(FLAP_W, CARD_H);
    const leftInsideMat = makeCardFaceMat(texInsideLeft);
    const leftInsideMesh = new THREE.Mesh(leftInsideGeo, leftInsideMat);
    leftInsideMesh.name = "panelLeft";
    leftInsideMesh.rotation.y = Math.PI;
    leftInsideMesh.position.z = -(HALF_THICK + 0.001);
    leftInsideMesh.castShadow = true;
    leftInsideMesh.receiveShadow = true;
    leftFlapGroup.add(leftInsideMesh);

    leftHinge.add(leftFlapGroup);
    cardGroup.add(leftHinge);

    // 3. RIGHT FLAP (Hinged at x = +2.5)
    rightHinge = new THREE.Group();
    rightHinge.name = "rightHinge";
    rightHinge.position.set(CARD_W / 2, 0, HALF_THICK);

    const rightFlapGroup = new THREE.Group();
    rightFlapGroup.position.set(-FLAP_W / 2, 0, 0);

    const rightBox = new THREE.Mesh(flapGeo, paperEdgeMat);
    rightBox.castShadow = true;
    rightBox.receiveShadow = true;
    rightFlapGroup.add(rightBox);

    // Front Exterior Face (Visible when CLOSED)
    const rightFrontGeo = new THREE.PlaneGeometry(FLAP_W, CARD_H);
    const rightFrontMat = makeCardFaceMat(texFrontRight);
    const rightFrontMesh = new THREE.Mesh(rightFrontGeo, rightFrontMat);
    rightFrontMesh.name = "frontRight";
    rightFrontMesh.position.z = HALF_THICK + 0.001;
    rightFrontMesh.castShadow = true;
    rightFrontMesh.receiveShadow = true;
    rightFlapGroup.add(rightFrontMesh);

    // Inside Interior Face (Visible when OPENED)
    const rightInsideGeo = new THREE.PlaneGeometry(FLAP_W, CARD_H);
    const rightInsideMat = makeCardFaceMat(texInsideRight);
    const rightInsideMesh = new THREE.Mesh(rightInsideGeo, rightInsideMat);
    rightInsideMesh.name = "panelRight";
    rightInsideMesh.rotation.y = Math.PI;
    rightInsideMesh.position.z = -(HALF_THICK + 0.001);
    rightInsideMesh.castShadow = true;
    rightInsideMesh.receiveShadow = true;
    rightFlapGroup.add(rightInsideMesh);

    rightHinge.add(rightFlapGroup);
    cardGroup.add(rightHinge);

    // Initial closed state as requested by user
    leftHinge.rotation.y = 0;
    rightHinge.rotation.y = 0;
  }

  // =========================================================================
  // CARD POSTURE: LIFT UP (STAND IN 3D) OR LAY FLAT (DESK MODE)
  // =========================================================================
  function applyCardPosture(deg, animate = true) {
    currentTiltDeg = deg;
    const rad = (90 - deg) * (Math.PI / 180); // 0° tilt = -90° (flat on desk); 90° tilt = 0° (upright vertical)
    const targetRotX = -rad;
    
    // Calculate Y height so the bottom edge rests naturally on the table (y = 0)
    // When deg = 90 (upright), height = CARD_H / 2 = 3.5
    // When deg = 0 (flat), height = HALF_THICK = 0.024
    const tiltRatio = deg / 90.0;
    const targetPosY = (CARD_H / 2) * Math.sin(deg * Math.PI / 180) + HALF_THICK;

    if (!animate) {
      cardGroup.rotation.x = targetRotX;
      cardGroup.position.y = targetPosY;
      return;
    }

    gsap.to(cardGroup.rotation, {
      x: targetRotX,
      duration: 1.4,
      ease: 'power2.inOut'
    });

    gsap.to(cardGroup.position, {
      y: targetPosY,
      duration: 1.4,
      ease: 'power2.inOut'
    });
  }

  function toggleLift() {
    isLifted = !isLifted;
    const targetTilt = isLifted ? 82 : 0;
    
    applyCardPosture(targetTilt, true);
    
    // Update slider position
    const slider = document.getElementById('tiltSlider');
    if (slider) slider.value = targetTilt;

    // Smoothly adjust camera and controls target
    if (isLifted) {
      gsap.to(controls.target, { x: 0, y: 3.5, z: 0, duration: 1.4, ease: 'power2.inOut' });
      gsap.to(camera.position, {
        x: isOpen ? VIEWS.openedCenter.pos.x : VIEWS.uprightPerspective.pos.x,
        y: isOpen ? VIEWS.openedCenter.pos.y : VIEWS.uprightPerspective.pos.y,
        z: isOpen ? VIEWS.openedCenter.pos.z : VIEWS.uprightPerspective.pos.z,
        duration: 1.4,
        ease: 'power2.inOut'
      });
    } else {
      // Resting Flat on Desk
      gsap.to(controls.target, { x: 0, y: 0, z: 0, duration: 1.4, ease: 'power2.inOut' });
      gsap.to(camera.position, {
        x: VIEWS.tableOverview.pos.x,
        y: VIEWS.tableOverview.pos.y,
        z: VIEWS.tableOverview.pos.z,
        duration: 1.4,
        ease: 'power2.inOut'
      });
    }

    updateLiftUI();
  }

  function updateLiftUI() {
    const btn = document.getElementById('btnLiftCard');
    const txt = document.getElementById('liftText');
    const ico = document.getElementById('liftIcon');
    const tiltVal = document.getElementById('tiltVal');

    if (isLifted) {
      if (btn) btn.classList.add('is-lifted');
      if (txt) txt.textContent = 'Lay Flat';
      if (ico) ico.textContent = '🛏️';
      if (tiltVal) tiltVal.textContent = `${currentTiltDeg}° (Standing 3D)`;
    } else {
      if (btn) btn.classList.remove('is-lifted');
      if (txt) txt.textContent = 'Lift Card';
      if (ico) ico.textContent = '🖐️';
      if (tiltVal) tiltVal.textContent = '0° (Flat on Table)';
    }
  }

  // =========================================================================
  // TOGGLE CARD OPEN / CLOSE (PHYSICAL GATEFOLD ANIMATION)
  // =========================================================================
  function toggleCard() {
    if (isAnimating) return;
    isAnimating = true;

    // Natural 3D wing angle: ~152 degrees (or currentFoldDeg) so flaps wing forward in 3D
    const targetRad = (currentFoldDeg * Math.PI) / 180;
    const targetAngle = isOpen ? 0 : targetRad;

    playPaperRustle();

    // Auto-start romantic music if not already playing
    if (!isOpen && !isMusicPlaying && cardAudio) {
      playSong();
    }

    const tl = gsap.timeline({
      onComplete: () => {
        isOpen = !isOpen;
        isAnimating = false;
        updateUI();

        if (isOpen && window.confetti) {
          triggerConfetti();
        }
      }
    });

    if (!isOpen) {
      // OPENING:
      // Left flap wings open
      tl.to(leftHinge.rotation, {
        y: -targetAngle,
        duration: 2.2,
        ease: 'power2.inOut'
      }, 0);

      // Right flap wings open with natural human offset
      tl.to(rightHinge.rotation, {
        y: targetAngle,
        duration: 2.25,
        ease: 'power2.inOut'
      }, 0.08);

      // Camera smoothly centers on the magnificent unfolded card
      const targetPos = isLifted ? VIEWS.openedCenter.pos : VIEWS.tableOverview.pos;
      const targetAim = isLifted ? VIEWS.openedCenter.target : VIEWS.tableOverview.target;

      tl.to(camera.position, {
        x: targetPos.x,
        y: targetPos.y,
        z: targetPos.z,
        duration: 2.3,
        ease: 'power2.inOut'
      }, 0);

      tl.to(controls.target, {
        x: targetAim.x,
        y: targetAim.y,
        z: targetAim.z,
        duration: 2.3,
        ease: 'power2.inOut'
      }, 0);

    } else {
      // CLOSING:
      tl.to(rightHinge.rotation, {
        y: 0,
        duration: 1.8,
        ease: 'power2.inOut'
      }, 0);

      tl.to(leftHinge.rotation, {
        y: 0,
        duration: 1.85,
        ease: 'power2.inOut'
      }, 0.05);

      const targetPos = isLifted ? VIEWS.uprightPerspective.pos : VIEWS.tableOverview.pos;
      const targetAim = isLifted ? VIEWS.uprightPerspective.target : VIEWS.tableOverview.target;

      tl.to(camera.position, {
        x: targetPos.x,
        y: targetPos.y,
        z: targetPos.z,
        duration: 1.9,
        ease: 'power2.inOut'
      }, 0);

      tl.to(controls.target, {
        x: targetAim.x,
        y: targetAim.y,
        z: targetAim.z,
        duration: 1.9,
        ease: 'power2.inOut'
      }, 0);
    }
  }

  // =========================================================================
  // ZOOM IN & ZOOM OUT CONTROLS (SMOOTH & INTUITIVE)
  // =========================================================================
  function zoomIn() {
    const dir = new THREE.Vector3().subVectors(controls.target, camera.position);
    const dist = dir.length();
    if (dist < 1.0) return; // Limit maximum close zoom
    
    const step = Math.min(2.0, dist * 0.32);
    dir.normalize().multiplyScalar(step);

    gsap.to(camera.position, {
      x: camera.position.x + dir.x,
      y: camera.position.y + dir.y,
      z: camera.position.z + dir.z,
      duration: 0.6,
      ease: 'power2.out'
    });
  }

  function zoomOut() {
    const dir = new THREE.Vector3().subVectors(camera.position, controls.target);
    const dist = dir.length();
    if (dist > 24.0) return; // Limit maximum far zoom
    
    const step = Math.min(2.5, dist * 0.35);
    dir.normalize().multiplyScalar(step);

    gsap.to(camera.position, {
      x: camera.position.x + dir.x,
      y: camera.position.y + dir.y,
      z: camera.position.z + dir.z,
      duration: 0.6,
      ease: 'power2.out'
    });
  }

  function focusSection(section) {
    if (!isOpen) {
      toggleCard();
    }

    if (!isLifted) {
      toggleLift();
    }

    let targetCam, targetAim;

    if (section === 'left') {
      targetAim = { x: -2.4, y: 3.5, z: 0.6 };
      targetCam = { x: -2.4, y: 3.5, z: 4.2 };
    } else if (section === 'heart') {
      targetAim = { x: 0.0, y: 3.4, z: 0.0 };
      targetCam = { x: 0.0, y: 3.4, z: 3.8 };
    } else if (section === 'right') {
      targetAim = { x: 2.4, y: 3.5, z: 0.6 };
      targetCam = { x: 2.4, y: 3.5, z: 4.2 };
    } else {
      // Whole Card
      targetAim = { x: 0.0, y: 3.5, z: 0.0 };
      targetCam = { x: 0.0, y: 3.6, z: 8.4 };
    }

    gsap.to(controls.target, {
      x: targetAim.x,
      y: targetAim.y,
      z: targetAim.z,
      duration: 1.4,
      ease: 'power2.inOut'
    });

    gsap.to(camera.position, {
      x: targetCam.x,
      y: targetCam.y,
      z: targetCam.z,
      duration: 1.4,
      ease: 'power2.inOut'
    });
  }

  function goToView(viewKey) {
    const v = VIEWS[viewKey];
    if (!v) return;

    gsap.to(camera.position, {
      x: v.pos.x,
      y: v.pos.y,
      z: v.pos.z,
      duration: 1.5,
      ease: 'power2.inOut'
    });

    gsap.to(controls.target, {
      x: v.target.x,
      y: v.target.y,
      z: v.target.z,
      duration: 1.5,
      ease: 'power2.inOut'
    });
  }

  // =========================================================================
  // ROMANTIC MUSIC & LOVE SONGS PLAYLIST ENGINE (7 Curated English Love Songs)
  // =========================================================================
  const LOVE_PLAYLIST = [
    {
      id: 'sailor',
      title: 'Sailor Song',
      artist: 'Gigi Perez',
      subtitle: 'Viral Romantic Ballad',
      file: 'audio/sailor_song.mp3',
      duration: '3:29',
      badge: 'Trending Love'
    },
    {
      id: 'her',
      title: 'Her',
      artist: 'JVKE',
      subtitle: 'Look at Her, She is a Masterpiece',
      file: 'audio/her_jvke.mp3',
      duration: '2:51',
      badge: 'Romantic'
    },
    {
      id: 'until_i_found_you',
      title: 'Until I Found You',
      artist: 'Stephen Sanchez',
      subtitle: 'Soulful Vintage Romance',
      file: 'audio/until_i_found_you.mp3',
      duration: '2:58',
      badge: 'Sweet & Pure'
    },
    {
      id: 'perfect',
      title: 'Perfect',
      artist: 'Ed Sheeran',
      subtitle: 'All-Time Romantic Classic',
      file: 'audio/perfect_ed_sheeran.mp3',
      duration: '4:23',
      badge: 'Favorite'
    },
    {
      id: 'dandelions',
      title: 'Dandelions',
      artist: 'Ruth B.',
      subtitle: 'Wishing on Every Dandelion',
      file: 'audio/dandelions_ruth_b.mp3',
      duration: '3:55',
      badge: 'Dreamy'
    },
    {
      id: 'golden_hour',
      title: 'Golden Hour',
      artist: 'JVKE',
      subtitle: 'She Got Glitter for Skin',
      file: 'audio/golden_hour_jvke.mp3',
      duration: '3:36',
      badge: 'Golden'
    },
    {
      id: 'cant_help_falling_in_love',
      title: "Can't Help Falling in Love",
      artist: 'Kina Grannis',
      subtitle: 'Acoustic Guitar Romance',
      file: 'audio/cant_help_falling_in_love.mp3',
      duration: '3:21',
      badge: 'Acoustic'
    }
  ];

  let currentSongIndex = 0;

  function setupAudio() {
    cardAudio = document.getElementById('cardAudio');
    volumeSlider = document.getElementById('volumeSlider');

    if (cardAudio) {
      cardAudio.volume = 0.85;
      cardAudio.addEventListener('ended', nextSong);
    }

    if (volumeSlider) {
      volumeSlider.addEventListener('input', (e) => {
        if (cardAudio) cardAudio.volume = parseFloat(e.target.value);
      });
    }

    // Prev / Play / Next track controls
    const btnPlayPause = document.getElementById('btnPlayPauseSong');
    if (btnPlayPause) btnPlayPause.addEventListener('click', toggleSong);

    const btnPrev = document.getElementById('btnPrevSong');
    if (btnPrev) btnPrev.addEventListener('click', prevSong);

    const btnNext = document.getElementById('btnNextSong');
    if (btnNext) btnNext.addEventListener('click', nextSong);

    // Playlist modal open triggers
    const btnOpenPlaylist = document.getElementById('btnOpenPlaylist');
    if (btnOpenPlaylist) btnOpenPlaylist.addEventListener('click', openSongModal);

    const btnBarPlaylist = document.getElementById('btnBarOpenPlaylist');
    if (btnBarPlaylist) btnBarPlaylist.addEventListener('click', openSongModal);

    const musicInfoClickable = document.getElementById('musicInfoClickable');
    if (musicInfoClickable) musicInfoClickable.addEventListener('click', openSongModal);

    // Modal close triggers
    const btnCloseModal = document.getElementById('btnCloseSongModal');
    if (btnCloseModal) btnCloseModal.addEventListener('click', closeSongModal);

    const modalBackdrop = document.getElementById('songModal');
    if (modalBackdrop) {
      modalBackdrop.addEventListener('click', (e) => {
        if (e.target === modalBackdrop) closeSongModal();
      });
    }

    // Custom song upload handlers (both top-nav and modal footer)
    const fileInput = document.getElementById('customAudioInput');
    const btnUpload = document.getElementById('btnUploadSong');
    const btnModalUpload = document.getElementById('btnModalUpload');

    const triggerUpload = () => {
      if (fileInput) fileInput.click();
    };

    if (btnUpload) btnUpload.addEventListener('click', triggerUpload);
    if (btnModalUpload) {
      btnModalUpload.addEventListener('click', () => {
        closeSongModal();
        triggerUpload();
      });
    }

    if (fileInput) {
      fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
          const objectUrl = URL.createObjectURL(file);
          cardAudio.src = objectUrl;
          playSong();

          const songName = file.name.replace(/\.[^/.]+$/, "");
          const titleEl = document.getElementById('songTitle');
          const subEl = document.getElementById('songSub');
          const badgeEl = document.getElementById('songBadge');
          if (titleEl) titleEl.textContent = songName;
          if (subEl) subEl.textContent = 'Custom Uploaded Song • Click to Change';
          if (badgeEl) badgeEl.textContent = 'Custom';

          document.querySelectorAll('.song-item').forEach(el => {
            el.classList.remove('is-selected', 'is-playing');
          });
        }
      });
    }

    // Render 6 curated songs and set default song display
    renderSongList();
    updateSongDisplay(0, false);
  }

  function renderSongList() {
    const container = document.getElementById('songListContainer');
    if (!container) return;

    container.innerHTML = '';
    LOVE_PLAYLIST.forEach((song, idx) => {
      const item = document.createElement('div');
      item.className = `song-item ${idx === currentSongIndex ? 'is-selected' : ''} ${idx === currentSongIndex && isMusicPlaying ? 'is-playing' : ''}`;
      item.dataset.index = idx;

      item.innerHTML = `
        <div class="song-item-idx">${idx + 1}</div>
        <div class="song-item-info">
          <div class="song-item-top">
            <span class="song-item-title">${song.title}</span>
            <span class="song-item-badge">${song.badge}</span>
          </div>
          <div class="song-item-artist">${song.artist} • ${song.subtitle}</div>
        </div>
        <div class="song-item-side">
          <div class="song-playing-anim">
            <span></span><span></span><span></span>
          </div>
          <span class="song-duration-tag">${song.duration}</span>
        </div>
      `;

      item.addEventListener('click', () => {
        selectSong(idx);
        closeSongModal();
      });

      container.appendChild(item);
    });
  }

  function updateSongDisplay(index, isPlayingNow = isMusicPlaying) {
    const song = LOVE_PLAYLIST[index];
    if (!song) return;

    const titleEl = document.getElementById('songTitle');
    const subEl = document.getElementById('songSub');
    const badgeEl = document.getElementById('songBadge');

    if (titleEl) titleEl.textContent = song.title;
    if (subEl) subEl.textContent = `${song.artist} • Click to Change Song ▾`;
    if (badgeEl) badgeEl.textContent = `Track ${index + 1}/${LOVE_PLAYLIST.length}`;

    // Update active states in modal list
    const items = document.querySelectorAll('.song-item');
    items.forEach((item, idx) => {
      if (idx === index) {
        item.classList.add('is-selected');
        if (isPlayingNow) item.classList.add('is-playing');
        else item.classList.remove('is-playing');
      } else {
        item.classList.remove('is-selected', 'is-playing');
      }
    });
  }

  function selectSong(index) {
    currentSongIndex = index;
    const song = LOVE_PLAYLIST[currentSongIndex];
    if (!song || !cardAudio) return;

    cardAudio.src = song.file;
    updateSongDisplay(currentSongIndex, true);
    playSong();
  }

  function nextSong() {
    const nextIdx = (currentSongIndex + 1) % LOVE_PLAYLIST.length;
    selectSong(nextIdx);
  }

  function prevSong() {
    const prevIdx = (currentSongIndex - 1 + LOVE_PLAYLIST.length) % LOVE_PLAYLIST.length;
    selectSong(prevIdx);
  }

  function openSongModal() {
    const modal = document.getElementById('songModal');
    if (modal) {
      modal.classList.add('active');
      modal.setAttribute('aria-hidden', 'false');
      updateSongDisplay(currentSongIndex, isMusicPlaying);
    }
  }

  function closeSongModal() {
    const modal = document.getElementById('songModal');
    if (modal) {
      modal.classList.remove('active');
      modal.setAttribute('aria-hidden', 'true');
    }
  }

  function playSong() {
    if (!cardAudio) return;
    cardAudio.play().then(() => {
      isMusicPlaying = true;
      updateMusicUI(true);
      updateSongDisplay(currentSongIndex, true);
    }).catch(() => {});
  }

  function pauseSong() {
    if (!cardAudio) return;
    cardAudio.pause();
    isMusicPlaying = false;
    updateMusicUI(false);
    updateSongDisplay(currentSongIndex, false);
  }

  function toggleSong() {
    if (isMusicPlaying) {
      pauseSong();
    } else {
      playSong();
    }
  }

  function updateMusicUI(playing) {
    const btnNav = document.getElementById('btnToggleMusic');
    const txtNav = document.getElementById('musicText');
    const btnPlay = document.getElementById('btnPlayPauseSong');
    const bar = document.getElementById('musicBar');

    if (playing) {
      if (btnNav) btnNav.classList.add('active');
      if (txtNav) txtNav.textContent = 'Pause Song';
      if (btnPlay) btnPlay.textContent = '⏸';
      if (bar) bar.classList.add('is-playing');
    } else {
      if (btnNav) btnNav.classList.remove('active');
      if (txtNav) txtNav.textContent = 'Play Song';
      if (btnPlay) btnPlay.textContent = '▶';
      if (bar) bar.classList.remove('is-playing');
    }
  }

  // Realistic Paper Rustle Sound
  function playPaperRustle() {
    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      const ctx = new AudioCtx();
      const bufferSize = ctx.sampleRate * 0.35;
      const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
      const data = buffer.getChannelData(0);
      for (let i = 0; i < bufferSize; i++) {
        data[i] = (Math.random() * 2 - 1) * Math.exp(-i / (ctx.sampleRate * 0.1));
      }
      const noise = ctx.createBufferSource();
      noise.buffer = buffer;
      const filter = ctx.createBiquadFilter();
      filter.type = 'bandpass';
      filter.frequency.value = 1100;
      filter.Q.value = 1.6;
      const gain = ctx.createGain();
      gain.gain.setValueAtTime(0.08, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.32);

      noise.connect(filter);
      filter.connect(gain);
      gain.connect(ctx.destination);
      noise.start();
    } catch (e) {}
  }

  // Confetti Celebration
  function triggerConfetti() {
    if (typeof confetti !== 'function') return;
    const colors = ['#f472b6', '#fb7185', '#fda4af', '#fde047', '#ffffff', '#e879f9'];
    confetti({
      particleCount: 85,
      spread: 85,
      origin: { y: 0.62 },
      colors: colors,
      disableForReducedMotion: true
    });
  }

  // =========================================================================
  // CURSOR-CENTERED ZOOM: ZOOM DIRECTLY TO MOUSE POINTER OR TOUCH PINCH POINT
  // =========================================================================
  const wheelRaycaster = new THREE.Raycaster();
  const wheelMouseNDC = new THREE.Vector2();
  const hitPlaneTarget = new THREE.Plane();
  const planeIntersectPoint = new THREE.Vector3();

  function zoomToScreenCoords(clientX, clientY, isZoomIn, factorMultiplier = 1.0) {
    const rect = renderer.domElement.getBoundingClientRect();
    wheelMouseNDC.x = ((clientX - rect.left) / rect.width) * 2 - 1;
    wheelMouseNDC.y = -((clientY - rect.top) / rect.height) * 2 + 1;

    wheelRaycaster.setFromCamera(wheelMouseNDC, camera);

    // 1. Raycast into all card objects (including meshes on left flap, right flap, center panel)
    const hits = wheelRaycaster.intersectObjects(cardGroup.children, true);
    const pivot = new THREE.Vector3();

    if (hits.length > 0) {
      // EXACT 3D point on the card surface under the cursor or touch point!
      pivot.copy(hits[0].point);
    } else {
      // Hovering outside the card: intersect with a plane at controls.target facing camera
      const camDir = new THREE.Vector3();
      camera.getWorldDirection(camDir);
      hitPlaneTarget.setFromNormalAndCoplanarPoint(camDir.negate(), controls.target);
      const hit = wheelRaycaster.ray.intersectPlane(hitPlaneTarget, planeIntersectPoint);
      if (hit) {
        pivot.copy(planeIntersectPoint);
      } else {
        pivot.copy(controls.target);
      }
    }

    const baseFactor = isZoomIn ? 0.82 : 1.22;
    const factor = Math.pow(baseFactor, factorMultiplier);

    const currentDist = camera.position.distanceTo(pivot);
    if (isZoomIn && currentDist < 0.40) return;  // Super close limit, prevents clipping
    if (!isZoomIn && currentDist > 30.0) return; // Outer boundary limit

    // Shift camera position along ray from pivot
    const newCamPos = new THREE.Vector3()
      .subVectors(camera.position, pivot)
      .multiplyScalar(factor)
      .add(pivot);

    // Also shift controls.target towards pivot proportionally
    // so orbiting centers around the zoomed area
    const newTarget = new THREE.Vector3()
      .subVectors(controls.target, pivot)
      .multiplyScalar(factor)
      .add(pivot);

    gsap.to(camera.position, {
      x: newCamPos.x,
      y: newCamPos.y,
      z: newCamPos.z,
      duration: 0.18,
      ease: 'power1.out',
      overwrite: 'auto'
    });

    gsap.to(controls.target, {
      x: newTarget.x,
      y: newTarget.y,
      z: newTarget.z,
      duration: 0.18,
      ease: 'power1.out',
      overwrite: 'auto'
    });
  }

  function onWheelZoomToCursor(e) {
    e.preventDefault();
    const isZoomIn = e.deltaY < 0;
    zoomToScreenCoords(e.clientX, e.clientY, isZoomIn, 1.0);
  }

  // =========================================================================
  // MOBILE TWO-FINGER PINCH-TO-ZOOM
  // =========================================================================
  let touchStartDist = 0;
  let lastTouchMidX = 0;
  let lastTouchMidY = 0;

  function onTouchStart(e) {
    if (e.touches.length === 2) {
      const t1 = e.touches[0];
      const t2 = e.touches[1];
      touchStartDist = Math.hypot(t1.clientX - t2.clientX, t1.clientY - t2.clientY);
      lastTouchMidX = (t1.clientX + t2.clientX) / 2;
      lastTouchMidY = (t1.clientY + t2.clientY) / 2;
      controls.enabled = false; // pause orbit while pinching
    }
  }

  function onTouchMove(e) {
    if (e.touches.length === 2) {
      e.preventDefault();
      const t1 = e.touches[0];
      const t2 = e.touches[1];
      const currentDist = Math.hypot(t1.clientX - t2.clientX, t1.clientY - t2.clientY);
      const midX = (t1.clientX + t2.clientX) / 2;
      const midY = (t1.clientY + t2.clientY) / 2;

      if (touchStartDist > 0 && Math.abs(currentDist - touchStartDist) > 3) {
        const isZoomIn = currentDist > touchStartDist;
        zoomToScreenCoords(midX, midY, isZoomIn, 0.45);
        touchStartDist = currentDist;
      }
    }
  }

  function onTouchEnd(e) {
    if (e.touches.length < 2) {
      touchStartDist = 0;
      controls.enabled = true; // resume orbit
    }
  }

  // =========================================================================
  // RAYCASTING: CLICK-TO-FOCUS & PHYSICAL TILT DRAGGING
  // =========================================================================
  const raycaster = new THREE.Raycaster();
  const mouse = new THREE.Vector2();
  let pointerDownTime = 0;
  let isDraggingTilt = false;
  let prevTiltMouseY = 0;

  function onPointerDown(e) {
    pointerDownTime = Date.now();
    prevTiltMouseY = e.clientY;

    // Shift + Left Click OR Middle Click initiates direct physical card tilt / lift
    if (e.shiftKey || e.button === 1) {
      isDraggingTilt = true;
      controls.enabled = false;
    }
  }

  function onPointerMove(e) {
    if (isDraggingTilt) {
      const deltaY = prevTiltMouseY - e.clientY; // dragging up = lift card upright
      prevTiltMouseY = e.clientY;
      const newTilt = Math.min(90, Math.max(0, currentTiltDeg + deltaY * 0.45));
      applyCardPosture(newTilt, false);
      isLifted = (newTilt > 25);
      updateLiftUI();
      const slider = document.getElementById('tiltSlider');
      if (slider) slider.value = newTilt;
      const tiltVal = document.getElementById('tiltVal');
      if (tiltVal) tiltVal.textContent = newTilt === 0 ? '0° (Flat)' : `${Math.round(newTilt)}° (Lifted)`;
    }
  }

  function onPointerUp(e) {
    if (isDraggingTilt) {
      isDraggingTilt = false;
      controls.enabled = true;
    }

    if (Date.now() - pointerDownTime > 220) return; // Drag action ignored

    const rect = renderer.domElement.getBoundingClientRect();
    mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(cardGroup.children, true);

    if (intersects.length > 0) {
      if (!isOpen) {
        toggleCard();
      }
    }
  }

  function onDoubleClick() {
    focusSection('center');
  }

  // =========================================================================
  // UI EVENT HANDLERS
  // =========================================================================
  function updateUI() {
    const btn = document.getElementById('btnToggleOpen');
    const txt = document.getElementById('openText');
    const ico = document.getElementById('openIcon');
    const hint = document.getElementById('interactionHint');

    if (isOpen) {
      if (btn) btn.classList.add('is-open');
      if (txt) txt.textContent = 'Close Card';
      if (ico) ico.textContent = '📕';
      if (hint) hint.innerHTML = '<span class="sparkle-icon">✨</span> Drag to orbit 360° • Click any note/photo to zoom close • Click "Close Card" to fold';
    } else {
      if (btn) btn.classList.remove('is-open');
      if (txt) txt.textContent = 'Open Card';
      if (ico) ico.textContent = '📖';
      if (hint) hint.innerHTML = '<span class="sparkle-icon">💖</span> Tap the card or click <strong>"Open Card"</strong> to unfold & reveal Siddhi\'s photos!';
    }
  }

  function setupEvents() {
    // 1. Lift Card Toggle Button
    const btnLift = document.getElementById('btnLiftCard');
    if (btnLift) btnLift.addEventListener('click', toggleLift);

    // 2. Open / Close Card
    const btnToggle = document.getElementById('btnToggleOpen');
    if (btnToggle) btnToggle.addEventListener('click', toggleCard);

    // 3. Music Toggle
    const btnMusic = document.getElementById('btnToggleMusic');
    if (btnMusic) btnMusic.addEventListener('click', toggleSong);

    // 4. Reset Camera View
    const btnReset = document.getElementById('btnResetView');
    if (btnReset) {
      btnReset.addEventListener('click', () => {
        goToView(isLifted ? (isOpen ? 'openedCenter' : 'uprightPerspective') : 'tableOverview');
      });
    }

    // 5. On-Screen Zoom Controls
    const btnZoomIn = document.getElementById('btnZoomIn');
    const btnZoomOut = document.getElementById('btnZoomOut');
    if (btnZoomIn) btnZoomIn.addEventListener('click', zoomIn);
    if (btnZoomOut) btnZoomOut.addEventListener('click', zoomOut);

    // 6. Focus Pill Buttons
    const btnFocusLeft = document.getElementById('btnFocusLeft');
    const btnFocusHeart = document.getElementById('btnFocusHeart');
    const btnFocusRight = document.getElementById('btnFocusRight');
    if (btnFocusLeft) btnFocusLeft.addEventListener('click', () => focusSection('left'));
    if (btnFocusHeart) btnFocusHeart.addEventListener('click', () => focusSection('heart'));
    if (btnFocusRight) btnFocusRight.addEventListener('click', () => focusSection('right'));

    // 7. Tilt & Lift Slider
    const tiltSlider = document.getElementById('tiltSlider');
    const tiltVal = document.getElementById('tiltVal');
    if (tiltSlider) {
      tiltSlider.addEventListener('input', (e) => {
        const val = parseInt(e.target.value, 10);
        applyCardPosture(val, false);
        isLifted = (val > 25);
        updateLiftUI();
        if (tiltVal) {
          tiltVal.textContent = val === 0 ? '0° (Flat)' : (val >= 80 ? `${val}° (Standing 3D)` : `${val}° (Tilted)`);
        }
      });
    }

    // 8. Flap Fold Angle Slider
    const foldSlider = document.getElementById('foldSlider');
    const foldVal = document.getElementById('foldVal');
    if (foldSlider) {
      foldSlider.addEventListener('input', (e) => {
        const deg = parseInt(e.target.value, 10);
        currentFoldDeg = deg;
        if (foldVal) {
          foldVal.textContent = deg === 180 ? '180° (Flat)' : `${deg}° (3D Wings)`;
        }
        if (isOpen) {
          const rad = (deg * Math.PI) / 180;
          leftHinge.rotation.y = -rad;
          rightHinge.rotation.y = rad;
        }
      });
    }

    // 9. Tilt Panel Minimize / Expand Toggle
    const btnToggleTiltPanel = document.getElementById('btnToggleTiltPanel');
    const tiltContent = document.getElementById('tiltPanelContent');
    if (btnToggleTiltPanel && tiltContent) {
      btnToggleTiltPanel.addEventListener('click', () => {
        const isHidden = tiltContent.style.display === 'none';
        tiltContent.style.display = isHidden ? 'block' : 'none';
        btnToggleTiltPanel.textContent = isHidden ? '▾' : '▸';
      });
    }

    // 10. Canvas Pointer, Wheel, Touch & Double-Click
    const dom = renderer.domElement;
    dom.addEventListener('wheel', onWheelZoomToCursor, { passive: false });
    dom.addEventListener('pointerdown', onPointerDown);
    dom.addEventListener('pointermove', onPointerMove);
    dom.addEventListener('pointerup', onPointerUp);
    dom.addEventListener('dblclick', onDoubleClick);

    // Mobile touch pinch-to-zoom
    dom.addEventListener('touchstart', onTouchStart, { passive: false });
    dom.addEventListener('touchmove', onTouchMove, { passive: false });
    dom.addEventListener('touchend', onTouchEnd);

    // 11. Mobile Audio Auto-Unlock on first touch gesture
    function unlockAudioOnFirstGesture() {
      if (cardAudio && !isMusicPlaying) {
        cardAudio.play().then(() => {
          isMusicPlaying = true;
          updateMusicUI(true);
        }).catch(() => {});
      }
      window.removeEventListener('touchstart', unlockAudioOnFirstGesture);
      window.removeEventListener('click', unlockAudioOnFirstGesture);
    }
    window.addEventListener('touchstart', unlockAudioOnFirstGesture, { once: true });
    window.addEventListener('click', unlockAudioOnFirstGesture, { once: true });

    // 12. Bottom Preset Buttons
    const presetBtns = document.querySelectorAll('.preset-btn');
    presetBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const viewKey = btn.dataset.view;
        presetBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        if (viewKey === 'tableOverview') {
          if (isLifted) toggleLift();
        } else if (['openedCenter', 'openedHeart', 'openedLeft', 'openedRight', 'uprightPerspective'].includes(viewKey)) {
          if (!isLifted) toggleLift();
          if (['openedCenter', 'openedHeart', 'openedLeft', 'openedRight'].includes(viewKey) && !isOpen) {
            toggleCard();
          }
          goToView(viewKey);
        } else {
          goToView(viewKey);
        }
      });
    });

    // 13. Keyboard Shortcuts (L = Lift, O = Open, M = Music, S = Song Modal, + = Zoom In, - = Zoom Out)
    window.addEventListener('keydown', (e) => {
      const key = e.key.toLowerCase();
      if (key === 'l') toggleLift();
      else if (key === 'o') toggleCard();
      else if (key === 'm') toggleSong();
      else if (key === 's') {
        const modal = document.getElementById('songModal');
        if (modal && modal.classList.contains('active')) closeSongModal();
        else openSongModal();
      }
      else if (e.key === 'Escape') closeSongModal();
      else if (e.key === '+' || e.key === '=') zoomIn();
      else if (e.key === '-' || e.key === '_') zoomOut();
      else if (key === 'r') goToView(isLifted ? 'openedCenter' : 'tableOverview');
    });

    window.addEventListener('resize', onWindowResize);
  }

  function onWindowResize() {
    const container = document.getElementById('webgl-container');
    const width = container.clientWidth || window.innerWidth;
    const height = container.clientHeight || window.innerHeight;

    const aspect = width / height;
    camera.aspect = aspect;

    // Responsive FOV: On vertical portrait mobile screens, expand FOV dynamically so the full width of the card fits!
    if (aspect < 1.0) {
      camera.fov = Math.min(68, Math.max(40, (40 / aspect) * 0.72));
    } else {
      camera.fov = 40;
    }

    camera.updateProjectionMatrix();
    renderer.setSize(width, height);
  }

  // =========================================================================
  // ANIMATION LOOP
  // =========================================================================
  function animate() {
    requestAnimationFrame(animate);

    controls.update();

    const time = Date.now() * 0.001;

    // Gentle Candlelight Flicker
    if (candleLight) {
      candleLight.intensity = 0.40 + Math.sin(time * 5.0) * 0.035;
    }

    // Floating Golden Dust Sparkles
    if (sparkleParticles) {
      const positions = sparkleParticles.geometry.attributes.position.array;
      for (let i = 0; i < positions.length; i += 3) {
        positions[i + 1] += Math.sin(time + positions[i]) * 0.0014;
      }
      sparkleParticles.geometry.attributes.position.needsUpdate = true;
    }

    renderer.render(scene, camera);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
