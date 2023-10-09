const setDetReportData = ({
    did,
    dname,
    active_module,
    module_count,
    contents,
    sentences,
}) => {
    const date = new Date();
    const report_data = {
        did: did,
        date: date.toLocaleDateString() + " " + date.toLocaleTimeString(),
        title: "Detection Report",
        title_fileName: dname,
        selected_modules: active_module,
        num_detected: {
            overview_typo: module_count.typo,
            overview_slang: module_count.slang,
            overview_dup: module_count.dup,
            overview_pdd: module_count.pdd,
            overview_spc: module_count.spc,
        },
        overview_all: calculate_overview_all(module_count),
        contents: contents,
        sentences: sentences,
    };
    return report_data;
};

const setConvReportData = ({
    did,
    dname,
    overview_rate,
    active_module,
    module_count,
    contents,
    converted_dname,
    converted_contents,
    details,
}) => {
    const date = new Date();
    const report_data = {
        did: did,
        date: date.toLocaleDateString() + " " + date.toLocaleTimeString(),
        title: "Conversion Report",
        title_fileName: dname,
        overview_rate: overview_rate,
        selected_modules: active_module,
        overview_all: calculate_overview_all(module_count),
        num_detected: {
            overview_typo: module_count.typo,
            overview_slang: module_count.slang,
            overview_dup: module_count.dup,
            overview_pdd: module_count.pdd,
            overview_spc: module_count.spc,
        },
        contents_original_fName: dname,
        contents_converted_fName: converted_dname,
        contents_original: contents.replace(/\n/g, "<br>"),
        contents_converted: converted_contents.replace(/\n/g, "<br>"),
        details: details,
    };
    return report_data;
};

// ========= functions ===========

function calculate_overview_all(module_count) {
    let overall = 0;
    for (let i in module_count) {
        if (!module_count[i]) {
            continue;
        }
        overall += module_count[i];
    }
    return overall;
}

export { setDetReportData as default, setConvReportData };
