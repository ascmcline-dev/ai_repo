import { app } from "../../../scripts/app.js";

const VARIANTS_URL = new URL("../shot_variants.json", import.meta.url);

const variantsReady = fetch(VARIANTS_URL)
    .then((response) => {
        if (!response.ok) {
            throw new Error(`Failed to load shot variants: ${response.status}`);
        }
        return response.json();
    })
    .then((data) => {
        if (!data || typeof data !== "object" || Array.isArray(data)) {
            throw new Error("shot_variants.json must contain an object");
        }
        return data;
    })
    .catch((error) => {
        console.error("[Dataset Shot Planner v1.7.0]", error);
        return {};
    });

function findWidget(node, name) {
    return node.widgets?.find((widget) => widget.name === name);
}

function setWidgetVisible(node, widget, visible) {
    if (!widget) return;

    if (!widget.__dspOriginalType) {
        widget.__dspOriginalType = widget.type;
        widget.__dspOriginalComputeSize = widget.computeSize;
    }

    if (visible) {
        widget.type = widget.__dspOriginalType;
        widget.computeSize = widget.__dspOriginalComputeSize;
    } else {
        widget.type = "hidden";
        widget.computeSize = () => [0, -4];
    }

    node.setSize?.([node.size[0], node.computeSize()[1]]);
    node.setDirtyCanvas?.(true, true);
}

function updateFemaleFields(node) {
    const gender = findWidget(node, "gender");
    const chest = findWidget(node, "female_chest_size");
    if (!gender || !chest) return;
    setWidgetVisible(node, chest, gender.value === "Female");
}

function updateOutfitFields(node) {
    const bodyVisibility = findWidget(node, "body_visibility");
    const outfitStyle = findWidget(node, "outfit_style");
    const outfitPriority = findWidget(node, "outfit_priority");
    const exactOutfit = findWidget(node, "exact_outfit");

    if (!bodyVisibility) return;

    const useSelectedOutfit = bodyVisibility.value === "Use Selected Outfit";
    setWidgetVisible(node, outfitStyle, useSelectedOutfit);
    setWidgetVisible(node, outfitPriority, useSelectedOutfit);
    setWidgetVisible(node, exactOutfit, useSelectedOutfit);
}

function repairSeed(node) {
    const randomSeed = findWidget(node, "random_seed");
    if (!randomSeed) return;

    const parsed = Number(randomSeed.value);
    if (!Number.isFinite(parsed) || !Number.isInteger(parsed) || parsed < 0) {
        randomSeed.value = 1985;
        randomSeed.callback?.(1985);
    }
}

function applyVariantFilter(node, variantsByType) {
    const shotType = findWidget(node, "shot_type");
    const shotVariant = findWidget(node, "shot_variant");
    if (!shotType || !shotVariant) return;

    const filteredValues = variantsByType[shotType.value] || [];
    if (!filteredValues.length) {
        console.warn(
            "[Dataset Shot Planner v1.7.0] No variants found for shot type:",
            shotType.value
        );
        return;
    }

    shotVariant.options = shotVariant.options || {};
    shotVariant.options.values = [...filteredValues];

    if (!filteredValues.includes(shotVariant.value)) {
        shotVariant.value = filteredValues[0];
        shotVariant.callback?.(shotVariant.value);
    }

    node.setDirtyCanvas?.(true, true);
}

app.registerExtension({
    name: "dataset_shot_planner.v1_7_0",

    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name !== "DatasetShotPlanner") return;

        const variantsByType = await variantsReady;
        const originalOnNodeCreated = nodeType.prototype.onNodeCreated;
        const originalOnConfigure = nodeType.prototype.onConfigure;
        const originalOnAdded = nodeType.prototype.onAdded;

        nodeType.prototype.onNodeCreated = function () {
            const result = originalOnNodeCreated?.apply(this, arguments);

            const shotType = findWidget(this, "shot_type");
            if (shotType && !shotType.__dspVariantCallbackInstalled) {
                shotType.__dspVariantCallbackInstalled = true;
                const previousCallback = shotType.callback;

                shotType.callback = (value) => {
                    previousCallback?.call(shotType, value);
                    applyVariantFilter(this, variantsByType);
                };
            }

            queueMicrotask(() => {
                repairSeed(this);
                applyVariantFilter(this, variantsByType);
                updateFemaleFields(this);
                updateOutfitFields(this);
            });

            return result;
        };

        nodeType.prototype.onConfigure = function () {
            const result = originalOnConfigure?.apply(this, arguments);

            queueMicrotask(() => {
                repairSeed(this);
                applyVariantFilter(this, variantsByType);
                updateFemaleFields(this);
                updateOutfitFields(this);
            });

            return result;
        };

        nodeType.prototype.onAdded = function () {
            const result = originalOnAdded?.apply(this, arguments);

            queueMicrotask(() => {
                applyVariantFilter(this, variantsByType);
                updateFemaleFields(this);
                updateOutfitFields(this);
            });

            return result;
        };
    },
});
