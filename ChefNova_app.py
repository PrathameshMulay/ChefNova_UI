                    substitution_lines.append(f"**{item}:** try {recipe['substitutions'][item]}")
            if substitution_lines:
                st.markdown("**Possible substitutions**")
                for line in substitution_lines:
                    st.markdown(f"- {line}")
        else:
            st.success("Cook now: every required ingredient is available in your confirmed pantry.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="small-note">AFTER COOKING</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:18px;font-weight:650;margin-top:8px;">How was this recipe?</div>', unsafe_allow_html=True)
        f1, f2, f3 = st.columns(3)
        if f1.button("👍 Loved", key=f"love_{recipe['id']}", use_container_width=True):
            st.session_state.feedback[recipe["id"]] = "Loved"
        if f2.button("😐 Okay", key=f"okay_{recipe['id']}", use_container_width=True):
            st.session_state.feedback[recipe["id"]] = "Okay"
        if f3.button("👎 No", key=f"no_{recipe['id']}", use_container_width=True):
            st.session_state.feedback[recipe["id"]] = "Disliked"
        if recipe["id"] in st.session_state.feedback:
            st.caption(f"Saved feedback: {st.session_state.feedback[recipe['id']]}. This can be used for future personalization.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Back to recommendations", use_container_width=True):
            st.session_state.page = "Recommendations"
            st.rerun()


# ---------- Evaluation plan ----------
def show_evaluation_plan():
    st.markdown('<div class="page-title">Evaluation Plan</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">A concrete testing plan addresses the feedback asking us to define receipt sources, recipe sources, and measurable accuracy targets.</div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Receipt test set</div>', unsafe_allow_html=True)
        st.markdown(
            """
            **Suggested sources**
            - Walmart
            - Target
            - Costco
            - Aldi
            - Instacart / grocery-order screenshots

            **Suggested conditions**
            - clear digital receipt
            - clear phone photo
            - slightly blurry / folded receipt
            - long receipt
            - mixed grocery + non-food receipt

            Start with **20–30 receipts** so the team can manually create ground-truth labels and calculate precision/recall.
            """
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Recipe source</div>', unsafe_allow_html=True)
        st.markdown(
            """
            **Current prototype:** ChefNova curated demo recipe dataset.

            **Next implementation choice:** replace or expand it with one clearly documented source such as:
            - Spoonacular API
            - TheMealDB
            - RecipeNLG / another licensed dataset

            Retrieval should happen **before** the LLM explanation step so ChefNova ranks grounded recipes instead of inventing every recipe from scratch.
            """
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Target metrics</div>', unsafe_allow_html=True)
    metric_df = pd.DataFrame(
        [
            ["Grocery item precision", "≥ 90%", "Of extracted grocery items, how many are truly groceries?"],
            ["Grocery item recall", "≥ 85%", "Of true grocery items, how many were extracted?"],
            ["Quantity extraction accuracy", "≥ 80%", "Was the quantity parsed correctly?"],
            ["Manual / voice parsing accuracy", "≥ 90%", "Did natural language become the correct structured items?"],
            ["Dietary compliance", "100% target", "Hard dietary filters should never be violated."],
            ["Cook-now feasibility", "≥ 95%", "Recipes labeled Cook now should truly require no missing core ingredients."],
            ["Top-3 recommendation relevance", "≥ 80% positive", "Users find at least one top recommendation acceptable."],
        ],
        columns=["Metric", "Target", "Meaning"],
    )
    st.dataframe(metric_df, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ---------- Router ----------
if st.session_state.page == "Home":
    show_home()
elif st.session_state.page == "My Inventory":
    show_inventory()
elif st.session_state.page == "Get Recipe":
    show_get_recipe()
elif st.session_state.page == "Recommendations":
    show_recommendations()
elif st.session_state.page == "Recipe Details":
    show_recipe_details()
elif st.session_state.page == "Evaluation Plan":
    show_evaluation_plan()
else:
    st.session_state.page = "Home"
    st.rerun()
