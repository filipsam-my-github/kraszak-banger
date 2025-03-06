#version 330 core
precision mediump float;

// Uniforms supplied by the application (e.g. via PyOpenGL)
uniform vec2 iResolution; // Window resolution (width, height)
uniform float iTime;      // Time in seconds

// Macros from the original shader code.
#define SS(x, y, z) smoothstep(x, y, z)
#define MD(a) mat2(cos(a), -sin(a), sin(a), cos(a))
#define PI (4.0 * atan(1.0))
#define TAU (2.0 * PI)
#define E exp(1.0)
#define resx (iResolution.xy / iResolution.y)

// --------------------------------------------------------------------
// Distance functions (SDFs)
// --------------------------------------------------------------------
float sdLine(in vec2 p, in vec2 a, in vec2 b) {
    vec2 pa = p - a;
    vec2 ba = b - a;
    float h = clamp(dot(pa, ba) / dot(ba, ba), 0.0, 1.0);
    return length(pa - ba * h);
}

float sdCircle(vec2 p, float r) {
    return length(p) - r;
}

float sdEllipse(in vec2 p, in vec2 ab) {
    p = abs(p);
    if (p.x > p.y) { 
        p = p.yx; 
        ab = ab.yx; 
    }
    float l = ab.y * ab.y - ab.x * ab.x;
    float m = ab.x * p.x / l;
    float m2 = m * m;
    float n = ab.y * p.y / l;
    float n2 = n * n;
    float c = (m2 + n2 - 1.0) / 3.0;
    float c3 = c * c * c;
    float q = c3 + m2 * n2 * 2.0;
    float d = c3 + m2 * n2;
    float g = m + m * n2;
    float co;
    if (d < 0.0) {
        float h = acos(q / c3) / 3.0;
        float s = cos(h);
        float t = sin(h) * sqrt(3.0);
        float rx = sqrt(-c * (s + t + 2.0) + m2);
        float ry = sqrt(-c * (s - t + 2.0) + m2);
        co = (ry + sign(l) * rx + abs(g) / (rx * ry) - m) / 2.0;
    } else {
        float h = 2.0 * m * n * sqrt(d);
        float s = sign(q + h) * pow(abs(q + h), 1.0/3.0);
        float u = sign(q - h) * pow(abs(q - h), 1.0/3.0);
        float rx = -s - u - c * 4.0 + 2.0 * m2;
        float ry = (s - u) * sqrt(3.0);
        float rm = sqrt(rx * rx + ry * ry);
        co = (ry / sqrt(rm - rx) + 2.0 * g / rm - m) / 2.0;
    }
    vec2 r = ab * vec2(co, sqrt(1.0 - co * co));
    return length(r - p) * sign(p.y - r.y);
}

float sdBox(in vec2 p, in vec2 b) {
    vec2 d = abs(p) - b;
    return length(max(d, vec2(0.0))) + min(max(d.x, d.y), 0.0);
}

// --------------------------------------------------------------------
// Letter distance functions
// --------------------------------------------------------------------
float l_D(vec2 p, float a) {
    float animl = SS(0.0, 1.0, a);
    float d1 = SS(0.002, 0.005, sdLine(p, vec2(0.0, 0.05), vec2(0.0, -0.15)));
    float d2 = SS(0.002, 0.005, abs(sdEllipse(p + vec2(0.0, 0.05), vec2(0.001 + 0.09 * animl, 0.1))));
    d2 = max(d2, step(p.x, 0.0));
    float d = min(d1, d2);
    d = max(d, 1.0 - step(0.25 - 0.25 * animl, -p.x + 0.24));
    return d;
}

float l_E(vec2 p, float a) {
    float animl = SS(0.0, 1.0, a);
    float d1 = SS(0.002, 0.005, sdLine(p, vec2(0.0, 0.05), vec2(0.0, -0.15)));
    d1 = max(d1, step(0.28 * animl, p.y + 0.2));
    float d2 = SS(0.002, 0.005, sdLine(p, vec2(0.0, -0.15), vec2(0.13, -0.15)));
    d2 = min(d2, SS(0.002, 0.005, sdLine(p, vec2(0.0, 0.05), vec2(0.13, 0.05))));
    d2 = min(d2, SS(0.002, 0.005, sdLine(p, vec2(0.0, -0.04), vec2(0.1, -0.04))));
    d2 = min(d2, SS(0.002, 0.005, sdLine(p, vec2(0.0, -0.06), vec2(0.1, -0.06))));
    d2 = max(d2, 1.0 - step(0.25 - 0.25 * animl, -p.x + 0.2));
    float d = min(d1, d2);
    d = max(d, 1.0 - step(0.25 - 0.25 * animl, -p.x + 0.2));
    return d;
}

float l_N(vec2 p, float a) {
    float animl = SS(0.0, 1.0, a);
    float d1 = SS(0.002, 0.005, sdLine(p, vec2(0.0, 0.0), vec2(0.1, -0.15)));
    d1 = min(d1, SS(0.002, 0.005, sdLine(p, vec2(0.0, 0.0), vec2(0.0, -0.15))));
    d1 = max(d1, step(0.25 * animl, p.y + 0.2));
    float d2 = SS(0.002, 0.005, sdLine(p, vec2(0.0, 0.05), vec2(0.135, -0.15)));
    d2 = min(d2, SS(0.002, 0.005, sdLine(p, vec2(0.135, -0.15), vec2(0.135, 0.05))));
    d2 = max(d2, step(0.28 * animl, -p.y + 0.1));
    float d = min(d1, d2);
    return d;
}

// --------------------------------------------------------------------
// Combined letter function
// --------------------------------------------------------------------
float func(vec2 p, float animx) {
    float d = 1.0;
    const float ax = -0.25;
    float ag = SS(0.0, 1.0, animx);
    float af = SS(6.0, 5.0, animx);
    const float fx = 0.255;
    float move_word = -0.20;
    
    d = SS(0.002, 0.005, sdLine(p, vec2(-1.0 + 2.5 * ag, -0.15), vec2(1.0 - 2.5 * af, -0.15)));
    animx += ax;
    d = min(d, l_E(p + vec2(0.195 + fx + move_word, -0.05), animx));
    animx += ax;
    d = min(d, l_N(p + vec2(0.05 + fx + move_word, -0.05), animx));
    animx += ax;
    d = min(d, l_D(p + vec2(-0.1 + fx + move_word, -0.05), animx));
    
    d *= 1.0 - step((p * MD(PI / 4.0)).x, 1.0 - 2.0 * af);
    return 1.0 - d;
}

// --------------------------------------------------------------------
// Colors (using normalized 0-1 values)
// --------------------------------------------------------------------
const vec3 col1_ = vec3(0x00, 0xcf, 0xc7) / 255.0;
const vec3 col2_ = vec3(0xff, 0x21, 0x78) / 255.0;
const vec3 black = vec3(0x00, 0x00, 0x00) / 255.0;
const vec3 white = vec3(0xfd, 0xfd, 0xfd) / 255.0;

// --------------------------------------------------------------------
// Main color function for a given point.
// --------------------------------------------------------------------
vec4 main_c(vec2 p) {
    vec3 col = vec3(0.0);
    float ax = mod(iTime, 7.0);
    const float av = -0.15;
    ax += av;
    float d3 = func(p, ax);
    ax += av;
    float d2 = func(p, ax);
    ax += av;
    float d = func(p, ax);
    
    vec3 col3 = mix(black, col2_, d3 - d2 + d);
    vec3 col2 = mix(black, col1_, d2);
    float af = SS(6.0, 5.0, ax);
    col = mix(black, white, d);
    col = max(col, col2);
    col = max(col, col3);
    col *= 1.0 - step((p * MD(PI / 4.0)).x, 1.0 - 2.0 * af);
    col *= vec3(SS(0.005, 0.002, sdBox(p, vec2(resx.x - 0.8, 0.2))));
    return vec4(col, 1.0);
}

// --------------------------------------------------------------------
// Fragment shader output variable
// --------------------------------------------------------------------
out vec4 FragColor;

void main() {
    // Map the fragment coordinate to UV space.
    // This centers the coordinate system by subtracting half of resx.
    vec2 uv = (gl_FragCoord.xy) / iResolution.y - resx / 2.0;
    uv *= 1.2;
    
    // Compute the final color and assign it to the output variable.
    FragColor = main_c(uv);
}
