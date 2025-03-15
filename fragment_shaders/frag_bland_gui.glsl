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
    vec4 base_color = texture(tex, uvs);

    // Apply glowing rectangle effects
    float glow_intensity1 = glowing_rectangle(uvs, hovered_button, time);
    vec3 hovered_button_glow_color = vec3(1.0, 1.0, 1.0);  // Bright white glow

    float glow_intensity2 = glowing_rectangle(uvs, chosen_button, time);
    vec3 chosen_button_glowColor = vec3(1.0, 0.6, 0.2);  // Orangish glow

    base_color.rbg += hovered_button_glow_color * glow_intensity1;
    base_color.rbg += chosen_button_glowColor * glow_intensity2;

    float adjusted_multiplayer = abs(transposition_shader_multiplayer);
    f_color = vec4(base_color.rgb * adjusted_multiplayer, 1.0);
}
