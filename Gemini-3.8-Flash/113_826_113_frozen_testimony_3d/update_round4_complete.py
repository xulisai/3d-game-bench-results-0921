import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Title Card description to mention mirrors and Q key
old_title_controls = """        <div class="card-controls-box">
          <b>CONTROLS:</b><br>
          &bull; <span class="keycap">W</span> <span class="keycap">A</span> <span class="keycap">S</span> <span class="keycap">D</span> &mdash; Walk the halls (2.5 units/s)<br>
          &bull; <b>Mouse</b> &mdash; Look and turn (click window to lock view)<br>
          &bull; <span class="keycap">E</span> &mdash; Examine glowing evidence (within 3 units)<br>
          &bull; <span class="keycap">J</span> &mdash; Open/close deduction journal (clickable constraint cards)<br>
          &bull; <span class="keycap">Tab</span> &mdash; Open/close Deduction Board (30 cells & contradiction markers)<br>
          &bull; <span class="keycap">Enter</span> &mdash; Begin the inquiry / Enter hall<br>
          &bull; <span class="keycap">R</span> &mdash; Reset anytime to this title card
        </div>"""

new_title_controls = """        <div class="card-controls-box">
          <b>CONTROLS:</b><br>
          &bull; <span class="keycap">W</span> <span class="keycap">A</span> <span class="keycap">S</span> <span class="keycap">D</span> &mdash; Walk the halls (2.5 units/s)<br>
          &bull; <b>Mouse</b> &mdash; Look and turn (click window to lock view)<br>
          &bull; <span class="keycap">E</span> &mdash; Examine glowing evidence (within 3 units)<br>
          &bull; <span class="keycap">Q</span> &mdash; Cycle Mirror Time View silhouettes (within 2 units of mirror)<br>
          &bull; <span class="keycap">J</span> &mdash; Open/close deduction journal (testimony & mirror sighting logs)<br>
          &bull; <span class="keycap">Tab</span> &mdash; Open/close Deduction Board (30 cells & contradiction markers)<br>
          &bull; <span class="keycap">Enter</span> &mdash; Begin the inquiry / Enter hall<br>
          &bull; <span class="keycap">R</span> &mdash; Reset anytime to this title card
        </div>"""

assert old_title_controls in html, "old_title_controls not matched"
html = html.replace(old_title_controls, new_title_controls)

# 2. Add Mirror HUD prompt and Time View banner HTML
old_interact_prompt = """    <div id="interact-prompt">Press <span class="keycap">E</span> to examine evidence</div>"""

new_interact_prompt = """    <div id="interact-prompt">Press <span class="keycap">E</span> to examine evidence</div>
    <div id="mirror-prompt" style="display: none; position: absolute; bottom: 125px; left: 50%; transform: translateX(-50%); background: rgba(14, 26, 44, 0.94); border: 1px solid #7ea2d6; border-radius: 4px; padding: 10px 22px; font-size: 14px; letter-spacing: 1.5px; color: #eaf1fa; box-shadow: 0 4px 20px rgba(0,0,0,0.75); pointer-events: none; z-index: 15; text-transform: uppercase;">
      Press <span class="keycap">Q</span> to cycle Mirror Time View (<span id="mirror-prompt-slot">Off</span>)
    </div>"""

assert old_interact_prompt in html, "old_interact_prompt not matched"
html = html.replace(old_interact_prompt, new_interact_prompt)

# Also add HUD mirror indicator badge in hud-bottom-bar
old_hud_bottom_controls = """        <span class="keycap">E</span> Examine &nbsp;|&nbsp;
        <span class="keycap">J</span> Journal &nbsp;|&nbsp;
        <span class="keycap">R</span> Title Reset"""

new_hud_bottom_controls = """        <span class="keycap">E</span> Examine &nbsp;|&nbsp;
        <span class="keycap">Q</span> Mirror Time View &nbsp;|&nbsp;
        <span class="keycap">J</span> Journal &nbsp;|&nbsp;
        <span class="keycap">R</span> Title Reset"""

assert old_hud_bottom_controls in html, "old_hud_bottom_controls not matched"
html = html.replace(old_hud_bottom_controls, new_hud_bottom_controls)

# Add mirror overlay card in body
old_examine_banner = """  <!-- Floating Examine Notification -->
  <div id="examine-banner">
    <div class="examine-header" id="banner-loc">Evidence Examined</div>
    <div class="examine-text" id="banner-text">Testimony text here</div>
    <div class="examine-footer">Added to Journal (<span class="keycap">J</span>)</div>
  </div>"""

new_examine_banner = """  <!-- Floating Examine Notification -->
  <div id="examine-banner">
    <div class="examine-header" id="banner-loc">Evidence Examined</div>
    <div class="examine-text" id="banner-text">Testimony text here</div>
    <div class="examine-footer">Added to Journal (<span class="keycap">J</span>)</div>
  </div>

  <!-- Mirror Time View Silhouette Overlay Banner -->
  <div id="mirror-banner" style="position: absolute; top: 90px; left: 50%; transform: translateX(-50%); background: linear-gradient(135deg, rgba(10, 18, 32, 0.94), rgba(16, 28, 48, 0.94)); border: 1px solid #6c8cb8; border-radius: 6px; padding: 16px 28px; box-shadow: 0 10px 40px rgba(0,0,0,0.9); z-index: 50; display: none; text-align: center; pointer-events: none; max-width: 680px;">
    <div style="font-size: 12px; letter-spacing: 3px; color: #a5c7f2; text-transform: uppercase; margin-bottom: 6px;" id="mirror-banner-header">Mirror Silhouette Tableau &bull; 19:00</div>
    <div style="font-size: 15px; line-height: 1.6; color: #f2f7fc; margin-bottom: 8px;" id="mirror-banner-text">The silhouette appears in the silvered glass...</div>
    <div style="font-size: 11px; letter-spacing: 1px; color: #8fa7c4;">Corroboration logged in Journal (<span class="keycap">J</span>) &bull; Press <span class="keycap">Q</span> to cycle time slot</div>
  </div>"""

assert old_examine_banner in html, "old_examine_banner not matched"
html = html.replace(old_examine_banner, new_examine_banner)

# 3. Add mirror journal section in journal-modal HTML
old_journal_ul = """      <ul class="testimony-list" id="journal-items-container">
        <!-- Injected -->
      </ul>"""

new_journal_ul = """      <ul class="testimony-list" id="journal-items-container">
        <!-- Injected -->
      </ul>

      <div style="margin-top: 24px; border-top: 1px solid #3c4f6d; padding-top: 18px;">
        <div style="font-size: 16px; font-weight: bold; color: #a5c7f2; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 12px;">
          Corridor Mirror Sightings (Seen Heading For)
        </div>
        <ul class="testimony-list" id="journal-mirror-container">
          <!-- Injected mirror sightings -->
        </ul>
      </div>"""

assert old_journal_ul in html, "old_journal_ul not matched"
html = html.replace(old_journal_ul, new_journal_ul)

# 4. Update GameState with mirror state
old_gamestate_block = """    const GameState = {
      mode: 'TITLE', // 'TITLE', 'EXPLORE', 'OPENED', 'STALLED'
      journalOpen: false,
      boardOpen: false,
      tickCount: 0,
      collectedIds: [],
      sampleAnswer: {
        answered: false,
        selected: null,
        correct: null
      },
      boardGrid: {
        butler:   { '19:00': '', '19:20': '', '19:40': '', '20:00': '', '20:20': '' },
        lady:     { '19:00': '', '19:20': '', '19:40': '', '20:00': '', '20:20': '' },
        doctor:   { '19:00': '', '19:20': '', '19:40': '', '20:00': '', '20:20': '' },
        maid:     { '19:00': '', '19:20': '', '19:40': '', '20:00': '', '20:20': '' },
        guest:    { '19:00': '', '19:20': '', '19:40': '', '20:00': '', '20:20': '' },
        gardener: { '19:00': '', '19:20': '', '19:40': '', '20:00': '', '20:20': '' }
      },
      collapseCount: 0,
      boardScore: null,
      activeInteractEvidence: null,
      bannerTimer: 0,
      highlightConstraint: null
    };"""

new_gamestate_block = """    const MIRROR_SCENES = [
      {
        slot: '19:00',
        person: 'butler',
        personName: 'the butler',
        room: 'kitchen',
        roomName: 'the kitchen',
        description: 'the butler crossing with a tray, making for the kitchen.',
        entryText: '19:00 — the butler was seen crossing with a tray, heading for the kitchen.'
      },
      {
        slot: '19:20',
        person: 'doctor',
        personName: 'the doctor',
        room: 'study',
        roomName: 'the study',
        description: 'the doctor heading for the study stairs.',
        entryText: '19:20 — the doctor was seen heading for the study stairs, making for the study.'
      },
      {
        slot: '19:40',
        person: 'lady',
        personName: 'the lady',
        room: 'drawing_room',
        roomName: 'the drawing room',
        description: 'the lady walking toward the drawing room.',
        entryText: '19:40 — the lady was seen walking toward the drawing room doorway.'
      },
      {
        slot: '20:00',
        person: 'gardener',
        personName: 'the gardener',
        room: 'kitchen',
        roomName: 'the kitchen',
        description: 'the gardener carrying a pail toward the kitchen.',
        entryText: '20:00 — the gardener was seen carrying a pail toward the kitchen.'
      },
      {
        slot: '20:20',
        person: 'guest',
        personName: 'the guest',
        room: 'garden',
        roomName: 'the garden',
        description: 'the guest stepping toward the garden door.',
        entryText: '20:20 — the guest was seen stepping toward the garden conservatory door.'
      }
    ];

    const GameState = {
      mode: 'TITLE', // 'TITLE', 'EXPLORE', 'OPENED', 'STALLED'
      journalOpen: false,
      boardOpen: false,
      tickCount: 0,
      collectedIds: [],
      seenMirrorSlots: [], // list of slot strings viewed e.g. ['19:00', ...]
      activeMirrorSlotIndex: -1, // -1 is off, 0..4 corresponds to MIRROR_SCENES
      sampleAnswer: {
        answered: false,
        selected: null,
        correct: null
      },
      boardGrid: {
        butler:   { '19:00': '', '19:20': '', '19:40': '', '20:00': '', '20:20': '' },
        lady:     { '19:00': '', '19:20': '', '19:40': '', '20:00': '', '20:20': '' },
        doctor:   { '19:00': '', '19:20': '', '19:40': '', '20:00': '', '20:20': '' },
        maid:     { '19:00': '', '19:20': '', '19:40': '', '20:00': '', '20:20': '' },
        guest:    { '19:00': '', '19:20': '', '19:40': '', '20:00': '', '20:20': '' },
        gardener: { '19:00': '', '19:20': '', '19:40': '', '20:00': '', '20:20': '' }
      },
      collapseCount: 0,
      boardScore: null,
      activeInteractEvidence: null,
      activeInteractMirror: null,
      bannerTimer: 0,
      highlightConstraint: null
    };"""

assert old_gamestate_block in html, "old_gamestate_block not matched"
html = html.replace(old_gamestate_block, new_gamestate_block)

# 5. Update updateArenaState to export mirror view and seen heading for sightings
old_arena_export = """        sample_answer_record: {
          answered: GameState.sampleAnswer.answered,
          selected: GameState.sampleAnswer.selected,
          correct: GameState.sampleAnswer.correct
        },
        deduction_board: {
          grid: JSON.parse(JSON.stringify(GameState.boardGrid)),
          collapse_count: GameState.collapseCount,
          score: GameState.boardScore,
          open: GameState.boardOpen
        }
      };"""

new_arena_export = """        sample_answer_record: {
          answered: GameState.sampleAnswer.answered,
          selected: GameState.sampleAnswer.selected,
          correct: GameState.sampleAnswer.correct
        },
        deduction_board: {
          grid: JSON.parse(JSON.stringify(GameState.boardGrid)),
          collapse_count: GameState.collapseCount,
          score: GameState.boardScore,
          open: GameState.boardOpen
        },
        corridor_mirrors: {
          active_time_slot: GameState.activeMirrorSlotIndex >= 0 ? MIRROR_SCENES[GameState.activeMirrorSlotIndex].slot : null,
          seen_heading_for_entries: GameState.seenMirrorSlots.map(s => {
            const sc = MIRROR_SCENES.find(m => m.slot === s);
            return sc ? { slot: sc.slot, person: sc.person, room: sc.room, log: sc.entryText } : null;
          }).filter(Boolean),
          near_mirror: !!GameState.activeInteractMirror
        }
      };"""

assert old_arena_export in html, "old_arena_export not matched"
html = html.replace(old_arena_export, new_arena_export)

print("Steps 1-5 replaced successfully")
with open('c4_step1.html', 'w', encoding='utf-8') as f:
    f.write(html)
