import streamlit as st
import requests
from collections import defaultdict
import io
from PIL import Image

# =============================
# CONFIG
# =============================
DETECT_API = "http://localhost:8000/detect"
GENERATE_API = "http://localhost:8000/generate"
CONF_THRESHOLD = 0.5

st.set_page_config(page_title="Photo → Recipe", layout="wide")

# =============================
# SESSION STATE INIT (CRITICAL)
# =============================
if "detected_items" not in st.session_state:
    st.session_state.detected_items = []

if "extra_items" not in st.session_state:
    st.session_state.extra_items = []

# =============================
# STYLES
# =============================
st.markdown("""
<style>
.title { font-size:40px; font-weight:700; }
.subtitle { font-size:18px; color:#666; }
.recipe-card {
    border:1px solid #ddd;
    border-radius:12px;
    padding:16px;
    margin-bottom:20px;
    background:#fafafa;
}
</style>
""", unsafe_allow_html=True)

# =============================
# HEADER
# =============================
st.markdown("""
<div class="title">📸 Photo → Recipe</div>
<div class="subtitle">
Upload or capture a food image. Detect ingredients → generate a recipe.
</div>
<hr>
""", unsafe_allow_html=True)

# =============================
# IMAGE INPUT
# =============================
left, right = st.columns([1, 1])

with left:
    source = st.radio(
        "Choose image source",
        ["Upload Image", "Use Camera"],
        horizontal=True
    )

    if source == "Upload Image":
        uploaded_file = st.file_uploader(
            "Upload food image",
            type=["jpg", "jpeg", "png"]
        )
    else:
        uploaded_file = st.camera_input("Capture food image")
        

        

# =============================
# DETECT INGREDIENTS
# =============================
if uploaded_file:
    st.image(uploaded_file, caption="Input Image", width="stretch")

    if st.button("🔍 Detect Ingredients"):
        with st.spinner("Detecting ingredients..."):
            files = {"file": uploaded_file.getvalue()}
            st.write("Image size (bytes):", len(uploaded_file.getvalue()))
            res = requests.post(DETECT_API, files=files)

            if res.status_code == 200:
                st.session_state.detected_items = res.json()["items"]
                st.session_state.extra_items = []  # reset extras on new detect
                st.success("Ingredients detected")
            else:
                st.error("Detection failed")


# =============================
# INGREDIENT CONFIRMATION
# =============================
final_items = []

if st.session_state.detected_items:
    st.subheader("🧾 Detected Ingredients")

    ingredient_stats = defaultdict(list)
    for item in st.session_state.detected_items:
        ingredient_stats[item["label"].lower()].append(item["score"])

    for i, (label, scores) in enumerate(ingredient_stats.items()):
        avg_conf = sum(scores) / len(scores)
        count = len(scores)

        cols = st.columns([3, 2, 2])
        with cols[0]:
            new_label = st.text_input(
                f"Ingredient {i+1}",
                value=label,
                key=f"ing_{i}"
            )
        with cols[1]:
            st.caption(f"Detected ×{count}")
            st.caption(f"Avg conf: {avg_conf:.2f}")
        with cols[2]:
            confirmed = True
            if avg_conf < CONF_THRESHOLD:
                confirmed = st.checkbox("Confirm?", key=f"conf_{i}")

        if confirmed and new_label.strip():
            final_items.append({
                "label": new_label.strip(),
                "score": round(avg_conf, 2)
            })

# =============================
# ADD EXTRA INGREDIENTS
# =============================
if st.session_state.detected_items:
    st.markdown("### ➕ Add Missing Ingredients (optional)")

    extra_input = st.text_input(
        "Enter extra ingredients (comma separated)",
        placeholder="e.g. ginger, turmeric, coriander"
    )

    if st.button("Add ingredients"):
        for e in extra_input.split(","):
            e = e.strip().lower()
            if e:
                st.session_state.extra_items.append({
                    "label": e,
                    "score": 1.0
                })
        st.success("Extra ingredients added")
# =============================
# MERGE FINAL ITEMS
# =============================
final_items.extend(st.session_state.extra_items)

if not final_items and st.session_state.detected_items:
    st.warning("Please confirm or add at least one ingredient.")
    st.stop()

# =============================
# RECIPE OPTIONS
# =============================
if final_items:
    st.subheader("⚙️ Recipe Options")

    opt1, opt2 = st.columns(2)
    with opt1:
        servings = st.number_input("Servings", 1, 10, 2)
    with opt2:
        cuisine = st.selectbox(
            "Cuisine Style",
            ["Indian", "Italian", "Chinese", "Mexican", "Continental"]
        )

# =============================
# GENERATE RECIPE
# =============================
if final_items and st.button("🍳 Generate Recipe"):
    payload = {
        "items": final_items,
        "servings": servings,
        "style": cuisine
    }

    with st.spinner("Cooking up ideas..."):
        res = requests.post(GENERATE_API, json=payload)

    if res.status_code != 200:
        st.error("Recipe generation failed")
        st.stop()

    recipe_data = res.json()
    st.toast("Recipe generated successfully 🍳", icon="✅")

    st.subheader("📖 Generated Recipes")


    # --- Metadata card ---
    meta = recipe_data.get("metadata", {})

    # st.markdown(f"""
    # <div class="recipe-card">
    #     <b>⏱️ Cook Time:</b> {meta.get("cook_time", "N/A")}<br>
    #     <b>🔥 Difficulty:</b> {meta.get("difficulty", "N/A")}<br>
    #     <b>🥗 Dietary:</b> {", ".join(meta.get("dietary", [])) or "N/A"}
    # </div>
    # """, unsafe_allow_html=True)

    # --- Ingredients table ---
    st.markdown("### 🧂 Ingredients")

    for ing in recipe_data.get("ingredients_list", []):
        st.markdown(f"- **{ing['name']}** — {ing['quantity']}")

    # --- Main recipe markdown ---
    st.markdown("### 👨‍🍳 Recipes")
    st.markdown(recipe_data["recipe_text"])


