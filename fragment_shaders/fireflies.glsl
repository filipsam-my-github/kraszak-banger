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

vec2 get_firefly_position_horizontal(float id, float time) {
    bool from_left = id < NUM_FIREFLIES_HORIZONTAL / 2;
    float baseX = from_left ? 0.0 : SCREEN_SIZE.x;
    float baseY = mod(id, 9.0) / 9.0 * SCREEN_SIZE.y + rand(vec2(id, 0.0)) * SCREEN_SIZE.y * 0.1;

    float speedFactor = 0.3;
    float twistAmount = 1.5;
    float spiralX = sin(time * speedFactor*1.3 + id * twistAmount) * SCREEN_SIZE.x;
    float spiralY = cos(time * speedFactor * 1.69 + id * twistAmount) * SCREEN_SIZE.y;


    if (from_left) spiralX = -spiralX;

    return vec2(baseX + spiralX, baseY + spiralY) / SCREEN_SIZE;
}

vec2 get_firefly_position_vertical(float id, float time) {
    bool from_left = id < NUM_FIREFLIES_VERTICAL / 2;
    float baseX = from_left ? 0.0 : SCREEN_SIZE.x;
    float baseY = mod(id, 9.0) / 9.0 * SCREEN_SIZE.y + rand(vec2(id, 0.0)) * SCREEN_SIZE.y * 0.1;

    float speedFactor = 0.3;
    float twistAmount = 1.5;
    float spiralX = sin(time * speedFactor + id * twistAmount) * SCREEN_SIZE.x * 0.2;
    float spiralY = cos(time * speedFactor * 1.3 + id * twistAmount) * SCREEN_SIZE.y * 0.15;

    if (from_left) spiralX = -spiralX;

    return vec2(baseX + spiralX, baseY + spiralY) / SCREEN_SIZE;
}

vec3 firefly_color(float id, float time) {
    float base_white = 0.8 + 0.2 * sin(time * 0.5 + id);
    float yellow_hint = 0.7 + 0.3 * cos(time * 0.3 + id);
    float blue_and_red = min(base_white, yellow_hint * 0.9) * 1.45;
    if (blue_and_red > 1) blue_and_red = 1.0;
    return vec3(base_white, blue_and_red, blue_and_red);
}

vec3 bigger_glow_color(float id, float time) {
    float yellow_hint = 0.6 + 0.2 * sin(time * 0.1 + id);
    float dimmer_white = 0.4 + 0.3 * cos(time * 0.1 + id);
    float blue_and_red = min(dimmer_white, yellow_hint * 0.8) * 1.25;
    if (blue_and_red > 1) blue_and_red = 1.0;
    return vec3(dimmer_white, blue_and_red, blue_and_red);
}

float glowing_rectangle(vec2 pos, vec4 rect, float time) {
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
    vec3 firefly_effect = baseColor.rgb;

    for (int i = 0; i < NUM_FIREFLIES_HORIZONTAL; i++) {
        float id = float(i);
        vec2 fireflyPos = get_firefly_position_horizontal(id, time);
        float distance = length(uvs - fireflyPos);
        float intensity = exp(-pow(distance * 15.0, 2.0)) * 1.2;
        float witherEffect = sin(time * 3.0 + id) * 0.5 + 0.5;
        intensity *= witherEffect;
        firefly_effect += firefly_color(id, time) * intensity;
        float bigger_glow_intensity = exp(-pow(distance * 25.0, 2.0)) * 0.5;
        firefly_effect += bigger_glow_color(id, time) * bigger_glow_intensity;
    }

    for (int i = 0; i < NUM_FIREFLIES_VERTICAL; i++) {
        float id = float(i);
        vec2 fireflyPos = get_firefly_position_vertical(id, time);
        float distance = length(uvs - fireflyPos);
        float intensity = exp(-pow(distance * 15.0, 2.0)) * 1.2;
        float witherEffect = sin(time * 3.0 + id) * 0.5 + 0.5;
        intensity *= witherEffect;
        firefly_effect += firefly_color(id, time) * intensity;
        float bigger_glow_intensity = exp(-pow(distance * 25.0, 2.0)) * 0.5;
        firefly_effect += bigger_glow_color(id, time) * bigger_glow_intensity;
    }

    firefly_effect = min(firefly_effect, vec3(1.0));

    // Apply glowing rectangle effects
    float glowIntensity1 = glowing_rectangle(uvs, hovered_button, time);
    vec3 hovered_button_glow_color = vec3(1.0, 1.0, 1.0);  // Bright white glow

    float glowIntensity2 = glowing_rectangle(uvs, chosen_button, time);
    vec3 chosen_button_glowColor = vec3(1.0, 0.6, 0.2);  // Orangish glow

    firefly_effect += hovered_button_glow_color * glowIntensity1;
    firefly_effect += chosen_button_glowColor * glowIntensity2;

    float adjusted_multiplayer = abs(transposition_shader_multiplayer);
    f_color = vec4(firefly_effect * adjusted_multiplayer, 1.0);
}
