({
    postMessageToChild: function (cmp, data) {
        const vfOrigin = "https://" + cmp.get("v.vfHost");
        const vfWindow = cmp.find("utiltyBarHelperFrame").getElement().contentWindow;
        data["source"] = "utilityBarHelper";
        vfWindow.postMessage(data, vfOrigin);
    }
});