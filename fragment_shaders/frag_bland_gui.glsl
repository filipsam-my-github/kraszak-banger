#version 330 core

uniform sampler2D tex;
uniform float time;
uniform vec4 hovered_button;
uniform vec4 chosen_button;
uniform float transposition_shader_multiplayer;

in vec2 uvs;
out vec4 f_color;

const vec2 SCREEN_SIZE = vec2(640.0, 360.0);
const float glowStrength = 1.0;
const float shrinkFactor = 250.0;
const float edgeSmoothness = 0.02;  // Controls how rounded the edges are
const float edgeDetection = 0.01;   // Threshold for detecting non-black pixels

// Function for glowing rectangles
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



// Function to check if a pixel is black
bool is_black(vec3 color) {
    return dot(color, vec3(1.0)) < edgeDetection;  // Check if almost black
}

// Function for glowing effect around non-black pixels with smooth edges
float text_glow(vec2 pos) {
    float glowEffect = 0.0;

    // Sample texture color at current position
    vec3 color = texture(tex, pos).rgb;

    // Only apply glow if the pixel is NOT black
    if (!is_black(color)) {
        // Distance from the top for vertical fade (adjustable)
        float distFromTop = 1 - pos.y;
        float baseGlow = glowStrength * exp(-pow((1.0 - distFromTop) * 2.0, 2.0) * shrinkFactor);

        // **Smooth Edge Effect**
        // Blend the glow smoothly around the pixel edges based on its x-position
        float leftEdge = smoothstep(0.0, edgeSmoothness, pos.x);
        float rightEdge = smoothstep(1.0, 1.0 - edgeSmoothness, pos.x);
        float edgeBlend = leftEdge * rightEdge;  // Both sides blend smoothly

        glowEffect += baseGlow * edgeBlend;
    }
    if (!is_black(color)) {
        // Distance from the top for vertical fade (adjustable)
        float distFromTop = pos.y;
        float baseGlow = glowStrength * exp(-pow((1.0 - distFromTop) * 2.0, 2.0) * shrinkFactor);

        // **Smooth Edge Effect**
        // Blend the glow smoothly around the pixel edges based on its x-position
        float leftEdge = smoothstep(0.0, edgeSmoothness, pos.x);
        float rightEdge = smoothstep(1.0, 1.0 - edgeSmoothness, pos.x);
        float edgeBlend = leftEdge * rightEdge;  // Both sides blend smoothly

        glowEffect += baseGlow * edgeBlend;
    }


    return clamp(glowEffect, 0.0, 1.0);
}
void main() {
    vec4 base_color = texture(tex, uvs);

    // Apply glowing rectangle effects
    float glow_intensity1 = glowing_rectangle(uvs, hovered_button, time);
    vec3 hovered_button_glow_color = vec3(1.0, 1.0, 1.0);  // Bright white glow

    float glow_intensity2 = glowing_rectangle(uvs, chosen_button, time);
    vec3 chosen_button_glowColor = vec3(1.0, 0.6, 0.2);  // Orangish glow

    base_color.rgb += hovered_button_glow_color * glow_intensity1;
    base_color.rgb += chosen_button_glowColor * glow_intensity2;

    // Apply glowing effect **only if pixel is NOT black**
    float glowEffect = text_glow(uvs);
    base_color.rgb += vec3(1.0, 1.0, 1.0) * glowEffect; 

    float adjusted_multiplayer = abs(transposition_shader_multiplayer);
    f_color = vec4(base_color.rgb * adjusted_multiplayer, 1.0);
}
