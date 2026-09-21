import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# -----------------------------------------------------------------------------
# 1. applyAxleLoadAndGetHeight: spanEnd for Level 3 = 48.0, support Lift Span on L2 or L3
# -----------------------------------------------------------------------------
old_axle_func = """    function applyAxleLoadAndGetHeight(axleX, loadWeight) {
      const currentSpanEnd = (activeLevel === 2 ? 36.0 : 24.0);
      if (axleX < 0 || axleX > currentSpanEnd) {
        return DECK_Y; // On solid grounded road stubs
      }
      for (let m = 0; m < members.length; m++) {
        const mem = members[m];
        if (mem.type !== 'deck' || mem.broken) continue;
        if (activeLevel === 2 && mem.isLiftSpan && liftSpanCurrentRaiseY > 0.1) continue;"""

new_axle_func = """    function applyAxleLoadAndGetHeight(axleX, loadWeight) {
      const currentSpanEnd = (activeLevel === 3 ? 48.0 : (activeLevel === 2 ? 36.0 : 24.0));
      if (axleX < 0 || axleX > currentSpanEnd) {
        return DECK_Y; // On solid grounded road stubs
      }
      for (let m = 0; m < members.length; m++) {
        const mem = members[m];
        if (mem.type !== 'deck' || mem.broken) continue;
        if ((activeLevel === 2 || activeLevel === 3) && mem.isLiftSpan && liftSpanCurrentRaiseY > 0.1) continue;"""

assert old_axle_func in html, "old_axle_func not found"
html = html.replace(old_axle_func, new_axle_func)

# -----------------------------------------------------------------------------
# 2. Lift span zero load in member physics
# -----------------------------------------------------------------------------
old_lift_phys = """        // Round 4: Lift Span Load Isolation!
        // While the lift span is active in Level 2 during the lift phase (raising, holding, or lowering),
        // it carries NO load and transmits NO force!
        if (activeLevel === 2 && mem.isLiftSpan && (activeStage === 'lift' || liftCyclePhase === 'raising' || liftCyclePhase === 'holding' || liftCyclePhase === 'lowering')) {
          mem.force = 0;
          mem.loadPct = 0;
          continue;
        }"""

new_lift_phys = """        // Lift Span Load Isolation (Level 2 & Level 3)
        // While the lift span is active during the lift phase (raising, holding, or lowering),
        // it carries NO load and transmits NO force!
        if ((activeLevel === 2 || activeLevel === 3) && mem.isLiftSpan && (activeStage === 'lift' || liftCyclePhase === 'raising' || liftCyclePhase === 'holding' || liftCyclePhase === 'lowering')) {
          mem.force = 0;
          mem.loadPct = 0;
          continue;
        }"""

assert old_lift_phys in html, "old_lift_phys not found"
html = html.replace(old_lift_phys, new_lift_phys)

# Lift span raised transform
old_lift_mesh = """          if (activeLevel === 2 && mem.isLiftSpan && liftSpanCurrentRaiseY > 0.001) {"""
new_lift_mesh = """          if ((activeLevel === 2 || activeLevel === 3) && mem.isLiftSpan && liftSpanCurrentRaiseY > 0.001) {"""

assert old_lift_mesh in html, "old_lift_mesh not found"
html = html.replace(old_lift_mesh, new_lift_mesh)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Simulation axle and lift physics updated successfully!")
