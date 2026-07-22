import { app } from "../../../scripts/app.js";

const OPTIONS_URL = new URL("../character_options.json", import.meta.url);

const optionsReady = fetch(OPTIONS_URL)
    .then((response) => {
        if (!response.ok) {
            throw new Error(`Failed to load character options: ${response.status}`);
        }
        return response.json();
    })
    .catch((error) => {
        console.error("[Standard Character Creator v1.5]", error);
        return {
            clothing_by_category: {},
            piercing_types_by_location: {},
        };
    });

function findWidget(node, name) {
    return node.widgets?.find((widget) => widget.name === name);
}

function setWidgetVisible(node, widget, visible) {
    if (!widget) return;

    if (!widget.__sccOriginalType) {
        widget.__sccOriginalType = widget.type;
        widget.__sccOriginalComputeSize = widget.computeSize;
    }

    if (visible) {
        widget.type = widget.__sccOriginalType;
        widget.computeSize = widget.__sccOriginalComputeSize;
    } else {
        widget.type = "hidden";
        widget.computeSize = () => [0, -4];
    }

    node.setSize?.([node.size[0], node.computeSize()[1]]);
    node.setDirtyCanvas?.(true, true);
}

function setComboValues(widget, values) {
    if (!widget || !Array.isArray(values) || values.length === 0) return;

    widget.options = widget.options || {};
    widget.options.values = [...values];

    if (!values.includes(widget.value)) {
        widget.value = values[0];
        widget.callback?.(widget.value);
    }
}

function updateGenderFields(node) {
    const gender = findWidget(node, "gender");
    const braBand = findWidget(node, "bra_band");
    const cupSize = findWidget(node, "cup_size");
    const breastShape = findWidget(node, "breast_shape");
    const breastPosition = findWidget(node, "breast_position");
    const breastFirmness = findWidget(node, "breast_firmness");
    const breastAugmentation = findWidget(node, "breast_augmentation");
    const maleGroin = findWidget(node, "male_groin_size");
    const femaleGroin = findWidget(node, "female_groin_description");

    if (!gender) return;

    const female = gender.value === "Adult Female";
    const male = gender.value === "Adult Male";

    setWidgetVisible(node, braBand, female);
    setWidgetVisible(node, cupSize, female);
    setWidgetVisible(node, breastShape, female);
    setWidgetVisible(node, breastPosition, female);
    setWidgetVisible(node, breastFirmness, female);
    setWidgetVisible(node, breastAugmentation, female);
    setWidgetVisible(node, femaleGroin, female);
    setWidgetVisible(node, maleGroin, male);
}

function updateHighlightFields(node) {
    const highlightStyle = findWidget(node, "highlight_style");
    const highlightColor = findWidget(node, "highlight_color");
    const customColor = findWidget(node, "custom_highlight_color");

    if (!highlightStyle) return;
    const visible = highlightStyle.value !== "None";

    setWidgetVisible(node, highlightColor, visible);
    setWidgetVisible(node, customColor, visible);
}

function updateHairColorFields(node) {
    const hairColor = findWidget(node, "hair_color");
    const customHairColor = findWidget(node, "custom_hair_color");

    if (!hairColor) return;
    const visible = ["Custom", "Vivid / Fantasy Color"].includes(hairColor.value);
    setWidgetVisible(node, customHairColor, visible);
}

function updateTattooFields(node) {
    const status = findWidget(node, "tattoo_status");
    const location = findWidget(node, "tattoo_location");
    const description = findWidget(node, "tattoo_description");

    if (!status) return;
    const visible = status.value !== "None";

    setWidgetVisible(node, location, visible);
    setWidgetVisible(node, description, visible);
}

function updatePiercingFields(node, shared) {
    const status = findWidget(node, "piercing_status");
    const location = findWidget(node, "piercing_location");
    const type = findWidget(node, "piercing_type");
    const notes = findWidget(node, "piercing_notes");

    if (!status) return;

    const visible = status.value !== "None";
    setWidgetVisible(node, location, visible);
    setWidgetVisible(node, type, visible);
    setWidgetVisible(node, notes, visible);

    if (visible && location && type) {
        const values = shared.piercing_types_by_location?.[location.value] || ["Unspecified"];
        setComboValues(type, values);
    }
}

function updateClothing(node, shared) {
    const category = findWidget(node, "clothing_category");
    const style = findWidget(node, "clothing_style");
    const exactClothing = findWidget(node, "exact_clothing");
    if (!category || !style) return;

    const values = shared.clothing_by_category?.[category.value] || ["Unspecified"];
    setComboValues(style, values);

    const noClothing = category.value === "No Clothing / Tattoo Documentation";
    setWidgetVisible(node, exactClothing, !noClothing);
}

function installCallback(widget, callback) {
    if (!widget || widget.__sccCallbackInstalled) return;

    widget.__sccCallbackInstalled = true;
    const previousCallback = widget.callback;

    widget.callback = function (value) {
        previousCallback?.call(widget, value);
        callback(value);
    };
}

app.registerExtension({
    name: "standard_character_creator.v1_5",

    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name !== "StandardCharacterCreator") return;

        const shared = await optionsReady;
        const originalOnNodeCreated = nodeType.prototype.onNodeCreated;
        const originalOnConfigure = nodeType.prototype.onConfigure;
        const originalOnAdded = nodeType.prototype.onAdded;

        function refresh(node) {
            updateGenderFields(node);
            updateHighlightFields(node);
            updateHairColorFields(node);
            updateTattooFields(node);
            updatePiercingFields(node, shared);
            updateClothing(node, shared);
        }

        function install(node) {
            installCallback(findWidget(node, "gender"), () => updateGenderFields(node));
            installCallback(findWidget(node, "highlight_style"), () => updateHighlightFields(node));
            installCallback(findWidget(node, "hair_color"), () => updateHairColorFields(node));
            installCallback(findWidget(node, "tattoo_status"), () => updateTattooFields(node));
            installCallback(findWidget(node, "piercing_status"), () => updatePiercingFields(node, shared));
            installCallback(findWidget(node, "piercing_location"), () => updatePiercingFields(node, shared));
            installCallback(findWidget(node, "clothing_category"), () => updateClothing(node, shared));
        }

        nodeType.prototype.onNodeCreated = function () {
            const result = originalOnNodeCreated?.apply(this, arguments);
            install(this);
            queueMicrotask(() => refresh(this));
            return result;
        };

        nodeType.prototype.onConfigure = function () {
            const result = originalOnConfigure?.apply(this, arguments);
            install(this);
            queueMicrotask(() => refresh(this));
            return result;
        };

        nodeType.prototype.onAdded = function () {
            const result = originalOnAdded?.apply(this, arguments);
            install(this);
            queueMicrotask(() => refresh(this));
            return result;
        };
    },
});
