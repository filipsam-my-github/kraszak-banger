#version 330 core

uniform sampler2D tex;
uniform float time;
uniform vec4 hovered_button;
uniform vec4 chosen_button;
uniform float transposition_shader_multiplayer;

in vec2 uvs;
out vec4 f_color;

const int NUM_FIREFLIES_HORIZONTAL = 60;
const int NUM_FIREFLIES_VERTICAL = 60;

const vec2 SCREEN_SIZE = vec2(640.0, 360.0);

float rand(vec2 co) {
    return fract(sin(dot(co.xy, vec2(12.9898, 78.233))) * 43758.5453);
}

vec2 getFireflyPositionHorizontal(float id, float time) {
    bool fromLeft = id < NUM_FIREFLIES_HORIZONTAL / 2;
    float baseX = fromLeft ? 0.0 : SCREEN_SIZE.x;
    float baseY = mod(id, 9.0) / 9.0 * SCREEN_SIZE.y + rand(vec2(id, 0.0)) * SCREEN_SIZE.y * 0.1;

    float speedFactor = 0.3;
    float twistAmount = 1.5;
    float spiralX = sin(time * speedFactor*1.3 + id * twistAmount) * SCREEN_SIZE.x;
    float spiralY = cos(time * speedFactor * 1.69 + id * twistAmount) * SCREEN_SIZE.y;


    if (fromLeft) spiralX = -spiralX;

    return vec2(baseX + spiralX, baseY + spiralY) / SCREEN_SIZE;
}

vec2 getFireflyPositionVertical(float id, float time) {
    bool fromLeft = id < NUM_FIREFLIES_VERTICAL / 2;
    float baseX = fromLeft ? 0.0 : SCREEN_SIZE.x;
    float baseY = mod(id, 9.0) / 9.0 * SCREEN_SIZE.y + rand(vec2(id, 0.0)) * SCREEN_SIZE.y * 0.1;

    float speedFactor = 0.3;
    float twistAmount = 1.5;
    float spiralX = sin(time * speedFactor + id * twistAmount) * SCREEN_SIZE.x * 0.2;
    float spiralY = cos(time * speedFactor * 1.3 + id * twistAmount) * SCREEN_SIZE.y * 0.15;

    if (fromLeft) spiralX = -spiralX;

    return vec2(baseX + spiralX, baseY + spiralY) / SCREEN_SIZE;
}

vec3 fireflyColor(float id, float time) {
    float baseWhite = 0.8 + 0.2 * sin(time * 0.5 + id);
    float yellowHint = 0.7 + 0.3 * cos(time * 0.3 + id);
    float blueAndRed = min(baseWhite, yellowHint * 0.9) * 1.45;
    if (blueAndRed > 1) blueAndRed = 1.0;
    return vec3(baseWhite, blueAndRed, blueAndRed);
}

vec3 biggerGlowColor(float id, float time) {
    float yellowHint = 0.6 + 0.2 * sin(time * 0.1 + id);
    float dimmerWhite = 0.4 + 0.3 * cos(time * 0.1 + id);
    float blueAndRed = min(dimmerWhite, yellowHint * 0.8) * 1.25;
    if (blueAndRed > 1) blueAndRed = 1.0;
    return vec3(dimmerWhite, blueAndRed, blueAndRed);
}

float glowingRectangle(vec2 pos, vec4 rect, float time) {
    float inRectX = step(rect.x, pos.x) * step(pos.x, rect.x + rect.z);
    float inRectY = step(rect.y, pos.y) * step(pos.y, rect.y + rect.w);
    float inRect = inRectX * inRectY;

    float edgeGlow = 0.02;
    float glowDistance = smoothstep(edgeGlow, 0.0, abs(pos.x - rect.x)) +
                         smoothstep(edgeGlow, 0.0, abs(pos.x - (rect.x + rect.z))) +
                         smoothstep(edgeGlow, 0.0, abs(pos.y - rect.y)) +
                         smoothstep(edgeGlow, 0.0, abs(pos.y - (rect.y + rect.w)));
    float flicker = 0.5 + 0.5 * sin(time * 5.0);
    return glowDistance * inRect * flicker;
}

void main() {
    vec4 baseColor = texture(tex, uvs);
    vec3 fireflyEffect = baseColor.rgb;

    for (int i = 0; i < NUM_FIREFLIES_HORIZONTAL; i++) {
        float id = float(i);
        vec2 fireflyPos = getFireflyPositionHorizontal(id, time);
        float distance = length(uvs - fireflyPos);
        float intensity = exp(-pow(distance * 15.0, 2.0)) * 1.2;
        float witherEffect = sin(time * 3.0 + id) * 0.5 + 0.5;
        intensity *= witherEffect;
        fireflyEffect += fireflyColor(id, time) * intensity;
        float biggerGlowIntensity = exp(-pow(distance * 25.0, 2.0)) * 0.5;
        fireflyEffect += biggerGlowColor(id, time) * biggerGlowIntensity;
    }

    for (int i = 0; i < NUM_FIREFLIES_VERTICAL; i++) {
        float id = float(i);
        vec2 fireflyPos = getFireflyPositionVertical(id, time);
        float distance = length(uvs - fireflyPos);
        float intensity = exp(-pow(distance * 15.0, 2.0)) * 1.2;
        float witherEffect = sin(time * 3.0 + id) * 0.5 + 0.5;
        intensity *= witherEffect;
        fireflyEffect += fireflyColor(id, time) * intensity;
        float biggerGlowIntensity = exp(-pow(distance * 25.0, 2.0)) * 0.5;
        fireflyEffect += biggerGlowColor(id, time) * biggerGlowIntensity;
    }

    fireflyEffect = min(fireflyEffect, vec3(1.0));

    // Apply glowing rectangle effects
    float glowIntensity1 = glowingRectangle(uvs, hovered_button, time);
    vec3 hoveredButtonGlowColor = vec3(1.0, 1.0, 1.0);  // Bright white glow

    float glowIntensity2 = glowingRectangle(uvs, chosen_button, time);
    vec3 chosenButtonGlowColor = vec3(1.0, 0.6, 0.2);  // Orangish glow

    fireflyEffect += hoveredButtonGlowColor * glowIntensity1;
    fireflyEffect += chosenButtonGlowColor * glowIntensity2;

    float adjusted_multiplayer = abs(transposition_shader_multiplayer);
    f_color = vec4(fireflyEffect * adjusted_multiplayer, 1.0);
}
