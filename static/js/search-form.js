const DATA = {
  weatherWebsites: [
    {
      name: "Weather Underground",
      url: "https://www.wunderground.com",
    },
    {
      name: "The Weather Channel",
      url: "https://weather.com",
    },
    {
      name: "Weather Bug",
      url: "https://www.weatherbug.com",
    },
  ],
  housingWebsites: [
    { name: "Zillow", url: "https://www.zillow.com" },
    {
      name: "Apartments.com",
      url: "https://www.apartments.com",
    },
  ],

  recipeWebsites: [
    {
      name: "Cook Pad",
      url: "https://www.cookpad.cow",
    },
    {
      name: "All Recipes",
      url: "https://www.allrecipes.com",
    },
    {
      name: "Food Network",
      url: "https://www.foodnetwork.com",
    },
  ],
};

const WEBSITE_SELECT_JOBJECT = $(".website-select");
const SEARCH_INPUT_JOBJECT = $(".search-input");
const CATEGORY_SELECT_JOBJECT = $(".category-select");
const SEARCH_BTN_JOBJECT = $(".search-form_btn");

(function init() {
  refreshWebsiteSelectJOBJECT();

  // handle search input's empty value upon typing and mouse leave action
  SEARCH_INPUT_JOBJECT.bind("mouseleave keyup", handleInputBlurMouseLeave);
  // handle category selections change event, which will update the website selection options.
  CATEGORY_SELECT_JOBJECT.bind("change", handleSelectChange);

  // this will rerender website selection when the web is refreshed or backwarded from the other website.
  $(this).bind("load", () => {
    refreshWebsiteSelectJOBJECT(); 
  })

})();

/**
 * Refreshes the search input's placeholder and website selection options.
 * @param {*} selectedVal
 * @returns
 */
function refreshWebsiteSelectJOBJECT() {
  const category = CATEGORY_SELECT_JOBJECT[0].value;
  // delete all the child element
  WEBSITE_SELECT_JOBJECT.empty();

  website_names = "";
  placeholder = "Please choose the category first.";
  // get website names and appropriate placeholder for category
  switch (category) {
    case "recipe":
      website_names = DATA.recipeWebsites.map((e) => e.name);
      placeholder = "Please enter the food's name.";
      break;
    case "weather":
      website_names = DATA.weatherWebsites.map((e) => e.name);
      console.log(website_names);
      placeholder = "Please enter your Zip code";

      break;
    case "housing":
      website_names = DATA.housingWebsites.map((e) => e.name);
      placeholder = "Please enter your Zip code";
      break;

    case "category":
      website_names = ["website"];
      break;

    default:
      alert("Something is wrong with the selection");
  }

  for (var website_name of website_names) {
    WEBSITE_SELECT_JOBJECT.append(
      `<option value="${website_name}"> ${website_name} </option>`
    );
  }

  // find jquery object of the input
  SEARCH_INPUT_JOBJECT.attr("placeholder", placeholder);
}
/**
 * Handler function for the search input.
 */
function handleInputBlurMouseLeave(e) {
  // input is not empty, category and website is selected.
  if (isValid()) {
    SEARCH_INPUT_JOBJECT.removeClass("warning");
    SEARCH_BTN_JOBJECT.prop("disabled", false);
  }
  // input is empty
  else {
    // make border red
    SEARCH_INPUT_JOBJECT.addClass("warning");
    // disable submit btn
    SEARCH_BTN_JOBJECT.prop("disabled", true);
  }
}

function handleSelectChange(e) {
  if (isValid()) {
    SEARCH_BTN_JOBJECT.prop("disabled", false);
    SEARCH_INPUT_JOBJECT.removeClass("warning");
  }
  // input is empty
  else {
    // make border red
    SEARCH_INPUT_JOBJECT.addClass("warning");
    // disable submit btn
    SEARCH_BTN_JOBJECT.prop("disabled", true);
  }

  refreshWebsiteSelectJOBJECT();
}

function isValid() {
  return (
    SEARCH_INPUT_JOBJECT[0].value != "" &&
    WEBSITE_SELECT_JOBJECT[0].value != "website" &&
    CATEGORY_SELECT_JOBJECT[0].value != "category"
  );
}
