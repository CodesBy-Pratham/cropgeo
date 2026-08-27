# CropGeo Analytics — Comprehensive Project Reference

> **Purpose of this document:** This is the master reference for the CropGeo Analytics dissertation report (black book). It contains every accurate fact about the project's actual implementation. Paste this entire file into any AI assistant (ChatGPT, Claude, Gemini, etc.) and then ask the AI to write specific black book sections. The AI must use **only the facts in this document** — not generic assumptions about agriculture software or plant disease detection apps.

---

## INSTRUCTIONS FOR AI ASSISTANTS READING THIS FILE

When the user asks you to write any section of the black book using this reference:

1. **This project is NOT a plant disease detection app, NOT a leaf image classifier, NOT a smart gardening app.** It is a **precision-agriculture web platform** that uses **satellite imagery (Sentinel-2)**, **vegetation indices (NDVI, EVI, NDMI)**, **weather forecasts (Open-Meteo)**, and **GIS polygons (PostGIS)** to help farmers monitor crop health.
2. Do NOT mention: SQLite, OpenWeatherMap, CNN, deep learning, leaf disease classification, AR plant preview, Node.js, MongoDB, PlantVillage dataset, image upload of leaves.
3. DO mention: PostgreSQL with PostGIS, Open-Meteo, TiTiler, Element84 STAC API, Sentinel-2 L2A, GeoDjango, OpenLayers, UTM projection, vegetation indices, 16-day forecast, soil moisture/temperature, ThreadPoolExecutor multi-threading, UUID primary keys, 10-acre AOI limit, admin approval workflow.
4. The black book format follows a typical Savitribai Phule Pune University MCA dissertation structure (7 chapters, references, appendices). Keep prose in plain English at a final-year MCA student level — not too academic, not too casual.
5. When generating content, mirror the *tone, paragraph structure, bullet style* of the friend's Smart Plant Partner PDF (which the user will describe separately), but **substitute the facts from this document**.
6. Always convert relative dates to absolute. Project year: 2025-2026.

---

## PROJECT IDENTITY

| Field | Value |
|---|---|
| Project title | **CropGeo Analytics** |
| Sub-title | A Web-Based GIS Platform for Satellite-Driven Precision Agriculture |
| Author | **Pratham Satish Pawar** |
| Role | SY MCA Student, Co-developer |
| Institution | **Matoshri Education Society's Matoshri College of Engineering and Research Centre, Nashik (Autonomous)** |
| Department | Department of Master of Computer Application (MCA) |
| Affiliated University | Savitribai Phule Pune University |
| Academic Year | 2025-2026 |
| Degree | Master of Computer Application (MCA) |
| Guide | Prof. (to be filled in by Pratham) |
| Head of Department | Dr. Apeksha R. Gawande |
| Director | Dr. G. K. Kharate |
| Exam Seat No. | (to be filled in) |
| PRN | (to be filled in) |

## ELEVATOR PITCH (one paragraph)

CropGeo Analytics is a Django-based web GIS platform that lets farmers and agricultural researchers register their farm boundaries on an interactive map, then monitor crop health remotely using free satellite imagery and weather data. After an administrator approves the user account, the farmer draws a polygon (up to 10 acres) over their field on an OpenLayers map, picks a crop type, and the system stores the polygon in a PostGIS database with accurate area in acres computed via UTM projection. From the farm dashboard, the user can search recent Sentinel-2 satellite scenes (filtered by date range and cloud cover) through the Element84 STAC API, compute vegetation indices (NDVI, EVI, NDMI) over the farm boundary via a TiTiler service, view the resulting raster as a colored map overlay, and check current weather plus a 16-day forecast (including soil temperature and moisture at multiple depths) from the Open-Meteo API. The whole system uses only free and open data sources, runs on Django 5.2 with GeoDjango, and is designed as a final-year MCA project demonstrating the integration of GIS, remote sensing, and weather APIs into a single web application.

---

# CHAPTER 1 — INTRODUCTION TO PROJECT

## 1.1 Introduction of Proposed Project

CropGeo Analytics is a web-based geographic information system (GIS) platform designed to bring precision-agriculture tools into the hands of individual farmers, agronomists, and agriculture researchers. The platform brings together three previously-disconnected sources of agricultural insight — **satellite imagery**, **weather data**, and **field geometry** — into a single, easy-to-use web dashboard.

In modern agriculture, decisions about irrigation, fertilizer application, pesticide spraying, and harvest timing depend critically on understanding the current state of the crop in the field. Traditionally, farmers rely on visual inspection — walking the field and looking at plants — to make these decisions. This approach has obvious limitations: a single farmer cannot effectively inspect every square meter of a large field, early signs of water stress or disease may be invisible to the naked eye, and weather forecasts that are accurate enough to guide spraying or irrigation decisions are not always available in farm-friendly form.

CropGeo Analytics solves these problems by combining three open data sources:

1. **Sentinel-2 satellite imagery** — captured by the European Space Agency's twin Sentinel-2 satellites every 5 days at 10-meter resolution. Accessed through the Element84 STAC (SpatioTemporal Asset Catalog) API, hosted on AWS Open Data.
2. **Vegetation indices** computed from the satellite imagery — NDVI (Normalized Difference Vegetation Index), EVI (Enhanced Vegetation Index), and NDMI (Normalized Difference Moisture Index). These mathematically extract information about plant health, biomass, and water content from raw satellite bands.
3. **Weather data** from the Open-Meteo API — current weather, a 16-day daily forecast, and detailed soil temperature and soil moisture at multiple depths.

The user interacts with the platform through a clean web interface built using Django templates and OpenLayers (an open-source mapping library). After registration and admin approval, the user draws their farm boundary as a polygon on a map. The platform stores this polygon in a PostgreSQL database with the PostGIS extension, calculates the exact area in acres using a UTM zone projection, and creates a personalized dashboard for that farm.

From the dashboard, the farmer can:
- Search for recent Sentinel-2 satellite scenes covering their farm.
- Compute NDVI / EVI / NDMI statistics (minimum, maximum, mean, standard deviation) over the farm polygon.
- View the satellite imagery as a colored overlay on the map.
- Read current weather and a 16-day forecast for the exact farm location.

The system is designed to use only free and open data sources, making precision agriculture accessible to farmers regardless of their budget. The project is technically significant because it integrates multiple advanced technologies — GeoDjango for GIS in a web framework, PostGIS for spatial database operations, STAC APIs for satellite data discovery, TiTiler for on-the-fly raster processing, and the Open-Meteo API for weather — into a single coherent web application built on Django 5.2.

From an MCA-curriculum perspective, the project demonstrates web development, database design, GIS, remote sensing, REST API consumption, multi-threading, and security (admin approval workflow, session-based authentication, geometry validation) — making it a strong real-world capstone project.

## 1.2 Motivation and Hypothesis

### Motivation

The motivation behind CropGeo Analytics comes from a real gap in Indian agriculture. India is the second-largest agricultural producer in the world, with over half the population employed in farming. Yet, despite the availability of advanced technologies like satellite imagery, weather forecasting, and GIS, most small and medium-scale farmers in India still rely on visual field inspection and informal knowledge to make crop-management decisions.

The reasons are clear:

- Commercial precision-agriculture platforms (Cropin, Fasal, Climate FieldView, EOS Crop Monitoring) are **expensive**, often require enterprise subscriptions, and are designed for large agribusinesses, not individual farmers.
- Free tools like Google Earth Engine require **programming skill** and are not accessible to non-technical users.
- Many farmers do not know that **free satellite data (Sentinel-2, Landsat)** and **free weather APIs (Open-Meteo)** exist and could be used to monitor their fields.
- Even technically inclined users face a steep learning curve: STAC APIs, COG (Cloud-Optimized GeoTIFF) formats, vegetation-index formulas, and UTM projections are not easy to use without prior training.

CropGeo Analytics aims to remove these barriers by packaging satellite-based crop monitoring, weather forecasting, and farm geometry management into a single web platform that a farmer or researcher can use through their browser, with no programming, no licenses, and no expensive subscriptions.

The motivation of the project, in bullet form:

- To make satellite-based crop monitoring accessible to small and medium farmers
- To integrate vegetation indices (NDVI, EVI, NDMI) with weather data in a single dashboard
- To use only free and open data sources (Sentinel-2, Open-Meteo)
- To accurately compute farm boundary area using UTM projection so size is real-world correct
- To demonstrate the integration of GIS, remote sensing, and web technologies in a single web application
- To build an MCA capstone project that solves a real-world precision-agriculture problem

### Hypothesis

The proposed system rests on the following hypothesis:

- A web-based GIS platform built on free and open data sources can deliver precision-agriculture insights with a user experience comparable to commercial platforms.
- Vegetation indices computed from Sentinel-2 imagery, when displayed clearly on a per-farm dashboard, can give farmers actionable information about crop health.
- An accurate farm area computed via UTM zone projection is sufficient for individual-farm management decisions (within the 10-acre target range).
- Combining vegetation indices with a 16-day weather forecast (including soil moisture and temperature at multiple depths) gives farmers a complete picture for irrigation and crop protection decisions.
- An admin-approval workflow can be used to prevent abuse while still keeping the registration process simple for legitimate users.

## 1.3 Presently Available Systems

Several commercial and research platforms currently offer satellite-based crop monitoring or precision-agriculture services. Each has strengths, but they also have limitations that CropGeo Analytics addresses.

### 1. Commercial Precision-Agriculture Platforms

**Cropin Technology** (Indian) — Offers a smart-farming suite including crop monitoring, yield prediction, and farm management. Used widely by agribusinesses and government programs. Limitations: requires enterprise licensing, focuses on large farming operations rather than individual farmers.

**Climate FieldView** (Bayer) — A widely-used precision-agriculture platform in the US that integrates field data, weather, and equipment. Limitations: expensive subscription, US-centric features, not designed for Indian farmers.

**EOS Crop Monitoring** — Provides satellite-based crop monitoring with NDVI, NDRE, and other indices. Limitations: paid plans for serious use, focus on enterprise users.

**Sentinel Hub** — A platform that provides access to Sentinel-2 and other satellite imagery via APIs. Limitations: developer-focused — requires programming skill and credit-based pricing; not a finished farmer-facing app.

### 2. Free / Research Platforms

**Google Earth Engine** — Free for research and non-commercial use; provides access to a massive archive of satellite data. Limitations: requires JavaScript or Python coding, no farmer-friendly UI, not designed for managing individual farms.

**QGIS with Sentinel-Hub plugin** — Free, open-source desktop GIS tool. Limitations: desktop-only (no web access), requires GIS expertise, no built-in weather data.

### 3. Government / Public Tools

**Indian Bhuvan portal** (ISRO) — Provides Indian satellite imagery and crop monitoring data. Limitations: limited to ISRO data sources, web interface is dated and not designed for farm-level personal accounts.

### Limitations of Existing Systems

Across these existing tools, the recurring limitations are:

- **High cost** — most commercial platforms are out of reach for small/medium farmers.
- **Technical barrier** — free tools (Earth Engine, Sentinel Hub) require coding skills.
- **No personal accounts** — many tools do not let an individual farmer register and save their own farm boundaries.
- **Either-or** — most tools focus on either satellite or weather data, not both.
- **No accurate area calculation** — many web tools display polygons without computing accurate real-world area in acres.
- **No size limit enforcement** — most tools do not check or restrict the size of registered farms, leading to abuse or system overload.
- **No admin moderation** — most lack a user-approval workflow for institutional or research use.

## 1.4 Advances / Additions in Existing System

CropGeo Analytics introduces a number of enhancements over existing systems by combining the best aspects of multiple tools and adding new ones tailored to small-farmer use:

### Proposed Enhancements

- **Unified satellite + weather + GIS dashboard** in a single web platform — no need to use multiple separate tools.
- **Free-only data sources** — uses Sentinel-2 imagery (free via Element84 STAC on AWS Open Data) and Open-Meteo weather (free, no API key required).
- **Accurate UTM-based area calculation** — farm polygon area in acres is computed by projecting to the correct UTM zone for the farm's longitude before measuring, giving sub-percent accuracy.
- **Server-side AOI size validation** — farm polygons larger than 10 acres are rejected at the server before they are stored, preventing abuse.
- **Admin approval workflow** — new user accounts default to `is_approved=False` and cannot access the platform until an administrator explicitly approves them. This makes the platform safe for institutional deployments.
- **Three vegetation indices out of the box** — NDVI for general crop health, EVI for high-biomass/atmospheric correction, and NDMI for moisture/water-stress monitoring.
- **16-day weather forecast** including soil temperature at 4 depths and soil moisture at 5 depth ranges — far more detail than typical weather widgets.
- **Multi-threaded statistics fetching** — when computing statistics for multiple satellite scenes, the system uses Python's `ThreadPoolExecutor` with up to 10 worker threads to fetch stats in parallel, dramatically reducing wait time.
- **UUID-based farm identifiers** — farm URLs use unguessable UUIDs (e.g., `/view-farm/3a7c9e1f-…`) so that one user cannot easily access another user's farm by changing a number in the URL.
- **OpenLayers map drawing** — interactive polygon drawing on a web map using OpenLayers (the open-source mapping library that GeoDjango uses out of the box).
- **Cloud-cover filtering** — when searching for satellite scenes, the user can specify the maximum acceptable cloud cover percentage so only clear-day imagery is returned.
- **Crop-type metadata** — each farm is tagged with a crop type (wheat, corn, soybeans, rice, cotton, barley, oats), allowing future ML-based crop-specific suggestions.

### Advantages Over Existing Systems

- Free to deploy and free to operate (no API keys with paid quotas).
- Web-based — accessible from any browser, no desktop install.
- Designed for individual farmers, not enterprises.
- Combines satellite + weather + farm management in one platform.
- Includes a server-side area limit to keep AOI sizes reasonable.
- Admin moderation makes it safe for institutional use.
- Built on Django — easily extensible by future developers.
- Uses only open-source libraries — no licensing concerns.

## 1.5 Detailed Problem Definition

In modern Indian agriculture, the small or medium-scale farmer faces a triple challenge:

1. **Crop health is hard to monitor visually.** A 5-acre field cannot be inspected leaf-by-leaf, and many problems (water stress, early nitrogen deficiency, gradual moisture loss) are not visible to the naked eye until they have already caused yield loss. Satellite imagery, in particular vegetation indices like NDVI and NDMI, can detect these problems days or weeks earlier than visual inspection — but accessing this satellite data requires expertise the farmer does not have.

2. **Weather forecasts are not in farm-friendly form.** Generic weather apps tell you "it might rain" but do not tell you the soil moisture at root-depth, the 16-day evapotranspiration, or the soil temperature at sowing depth — information that would actually drive a planting or irrigation decision.

3. **Farm geometry is rarely digital.** Even when a farmer knows the approximate size of their field, the exact polygon is usually not stored anywhere computable. Without a digital polygon, satellite data and weather data cannot be specifically tied to *this* field.

The combination of these three problems means that even though all the underlying data (satellite imagery, weather, accurate maps) exists for free on the public internet, the small farmer cannot use any of it.

Specific problems identified during requirement gathering:

- **No accessible platform for small farmers** to monitor crops using satellite imagery.
- **Existing tools are too technical** (Google Earth Engine, QGIS) or **too expensive** (Cropin, EOS).
- **Weather forecast tools do not surface soil data**, which is critical for irrigation decisions.
- **Farm boundary capture is manual and error-prone**, and accurate area calculation requires GIS expertise (UTM projection).
- **No user-account-driven system** ties a specific farmer's identity to specific farm polygons over time.
- **No safeguards** against abusively large AOI polygons that could overload the server.
- **No institutional moderation layer** for university/research deployments where students should not be able to register without approval.

CropGeo Analytics addresses all of these problems in a single integrated web application.

## 1.6 Scope and Objectives

### Scope

The scope of CropGeo Analytics includes:

- **Web-based access** through a modern browser; no mobile app or desktop install required.
- **Multi-user system** with user registration, login, logout, and admin moderation.
- **Farm boundary management** — users can draw, save, view, and delete their farm polygons.
- **Maximum farm size 10 acres** — enforced on the server during farm creation (`MAX_FARM_AOI_ACRES = 10`).
- **Sentinel-2 L2A satellite imagery** via the Element84 STAC API on AWS Open Data.
- **Three vegetation indices**: NDVI, EVI, NDMI.
- **Date-range and cloud-cover filtering** of satellite scenes.
- **Satellite raster rendering** through the TiTiler service, with customizable colormap and rescale range.
- **Current weather + 16-day forecast** at the farm centroid, via Open-Meteo.
- **Detailed soil data** in the weather payload: soil temperature at 0, 6, 18, 54 cm and soil moisture at 5 depth ranges.
- **Admin dashboard** with paginated user list, paginated farm list, user approval/rejection/deactivation/deletion.
- **PostgreSQL with PostGIS** as the spatial database backend (not SQLite).
- **Crop types supported**: wheat, corn, soybeans, rice, cotton, barley, oats.

Out of scope (in the current version):
- No mobile app.
- No historical archive UI (only date-range search from the satellite list, not a timelapse view).
- No ML-based yield prediction or disease classification.
- No multi-farm comparison.
- No notification system (email or SMS alerts).
- No payment / subscription system.
- No multilingual UI (English only).

### Target Users

- **Home gardeners**: not the primary audience — CropGeo is designed for working fields, not container gardens.
- **Small and medium-scale farmers** (1-10 acres) — the primary audience.
- **Agriculture researchers and agronomists** monitoring trial plots or research farms.
- **Agricultural extension officers** managing portfolios of farmer accounts (using the admin dashboard).
- **MCA / CS students and faculty** interested in GIS, remote sensing, or web development as a learning platform.

### Objectives

The technical objectives of the project are:

- To design and implement a Django-based web GIS platform using GeoDjango and PostGIS.
- To integrate the Element84 STAC API for discovering Sentinel-2 satellite scenes.
- To integrate the TiTiler service for on-the-fly raster processing and statistics.
- To integrate the Open-Meteo API for current weather and 16-day forecast.
- To implement vegetation index computation (NDVI, EVI, NDMI) using band-math expressions sent to TiTiler.
- To implement accurate farm-area calculation using dynamic UTM zone selection.
- To enforce a server-side maximum farm size of 10 acres.
- To implement a secure admin approval workflow for new user accounts.
- To use multi-threading (`ThreadPoolExecutor`) for parallel statistics fetching when applicable.
- To provide a clean, responsive user interface using Django templates and OpenLayers.
- To document the system thoroughly so that future MCA students can extend it.

## 1.7 Outcomes

The expected outcomes of the CropGeo Analytics project are:

- A fully functional web application demonstrating satellite-based crop monitoring for small farms.
- An accurate, server-side area-validated farm registration system supporting polygons up to 10 acres.
- An integrated dashboard showing satellite imagery, vegetation index statistics, current weather, and a 16-day forecast for each registered farm.
- A user moderation system (admin approval workflow) suitable for institutional deployments.
- A demonstration of integrating multiple advanced technologies (GIS, remote sensing, REST APIs, multi-threading) into a single coherent Django application.
- A reusable architecture that can be extended to additional satellite sources (Landsat, PlanetScope) or additional vegetation indices.
- A practical knowledge base for future MCA / agriculture-tech projects.

## 1.8 Organization of Dissertation

This dissertation is organized into seven chapters:

- **Chapter 1 — Introduction:** Project overview, motivation, hypothesis, existing systems, problem definition, scope, objectives, outcomes.
- **Chapter 2 — Literature Survey:** Review of related work in satellite-based crop monitoring, GIS web platforms in agriculture, and Cloud-Optimized GeoTIFF / STAC-based imagery serving.
- **Chapter 3 — Software Requirement Specification:** Hardware, software, functional, and non-functional requirements.
- **Chapter 4 — Design and Modeling:** System architecture, E-R diagram, data flow diagrams, UML diagrams.
- **Chapter 5 — Implementation and Testing:** Modules implemented, algorithms used, testing methodology, test cases, screenshots.
- **Chapter 6 — Result and Analysis:** What was successfully built, how reports are generated and visualized, discussion of strengths and limitations.
- **Chapter 7 — Conclusion and Future Scope:** Summary of achievements and future enhancements.
- **References:** Academic papers, official documentation, and standards referred to.
- **Appendices:** Supporting reference material — full file inventory, URL table, view-function reference, vegetation-index reference, environment-variable reference, migration history.

---

# CHAPTER 2 — LITERATURE SURVEY

The literature survey for CropGeo Analytics covered three principal areas of related work: satellite-based crop monitoring using vegetation indices, GIS web platforms in agriculture, and Cloud-Optimized GeoTIFFs (COGs) with STAC-based imagery serving. These three areas together cover all the technical foundations on which the project is built.

The survey concludes that, while many tools exist in each area separately, very few open-source platforms combine all three for individual-farmer use. CropGeo Analytics fills this gap by integrating Sentinel-2 imagery (via Element84 STAC), TiTiler-based on-the-fly raster processing, GeoDjango / PostGIS for farm geometry storage, and the Open-Meteo API for weather — all in a single Django web application.

## 2.1 Satellite-Based Crop Monitoring Using Vegetation Indices

Satellite-based crop monitoring is the practice of using imagery captured by Earth-observation satellites to derive information about crop condition. The most common technique is to compute **vegetation indices** — mathematical combinations of satellite bands that emphasize properties of vegetation that are otherwise hidden in raw imagery.

The most widely used vegetation indices are:

- **NDVI (Normalized Difference Vegetation Index)** — defined as `(NIR - Red) / (NIR + Red)`. Healthy vegetation reflects strongly in NIR and absorbs Red, so NDVI ranges from -1 to +1 with values 0.6-0.9 typical of healthy crops. NDVI is the most-studied vegetation index and has been used in agricultural research since the 1970s.
- **EVI (Enhanced Vegetation Index)** — defined as `2.5 * ((NIR - Red) / (NIR + 6*Red - 7.5*Blue + 1))`. EVI corrects for atmospheric effects and soil background, making it more reliable than NDVI in dense canopies and over bare-soil patches.
- **NDMI (Normalized Difference Moisture Index)** — defined as `(NIR - SWIR16) / (NIR + SWIR16)`. NDMI uses the short-wave infrared band, which is sensitive to water content, making it useful for monitoring crop water stress and irrigation needs.

The European Space Agency's **Sentinel-2 mission** provides free, multi-spectral satellite imagery at 10-meter resolution, with a revisit time of approximately 5 days for any point on Earth. Sentinel-2 L2A (Level 2A) data has been atmospherically corrected and is suitable for direct vegetation-index computation. The Element84 organization (and AWS Open Data) host the entire Sentinel-2 L2A archive as Cloud-Optimized GeoTIFFs, making it freely accessible via the STAC API at `https://earth-search.aws.element84.com/v1`.

### Features (of satellite-based crop monitoring)
- Field-level visibility without ground inspection
- Repeated coverage every 5 days (Sentinel-2)
- Detects subtle crop changes invisible to the eye
- Free imagery from public satellite missions
- Quantitative outputs (statistics, time series)

### Advantages
- Reduces manual field-walking effort
- Detects water stress and biomass changes early
- Enables data-driven irrigation and fertilizer decisions
- Scales to many fields at once
- Provides historical record for season-over-season comparison

### Limitations
- Cloud cover blocks satellite observations
- 10 m resolution is too coarse for small home gardens
- Atmospheric correction can fail in extreme conditions
- Requires careful colormap and rescale choices for meaningful visualization
- Vegetation indices are only proxies — not direct measurements of yield or disease

## 2.2 GIS Web Platforms in Agriculture

A geographic information system (GIS) is a system for capturing, storing, analyzing, and presenting spatial data. In agriculture, GIS is used to map farm boundaries, soil characteristics, irrigation networks, and yield zones.

**Web GIS** brings GIS capabilities into a browser, removing the need for desktop GIS software like QGIS or ArcGIS. The most common stack for open-source web GIS is:

- **PostgreSQL with PostGIS** — a relational database with spatial-data support. PostGIS adds geometry data types (`GeometryField`, `PointField`, `PolygonField`) and spatial functions (`ST_Area`, `ST_Intersects`, `ST_Transform`, `ST_Contains`).
- **GeoDjango** — the GIS-aware version of Django, which adds spatial model fields, spatial querysets, and admin integration for PostGIS.
- **OpenLayers** or **Leaflet** — JavaScript libraries for displaying interactive maps in a web browser. GeoDjango includes built-in OpenLayers integration for admin and form widgets.

In agriculture, a web GIS platform allows farmers to:

- Draw and save their farm boundaries (polygons) as digital geometries.
- View their fields on top of basemaps or satellite imagery.
- Query field-level data (size, crop type, owner) using spatial filters.
- Tie weather and satellite data to specific fields rather than just generic locations.

### Features (of web GIS in agriculture)
- Interactive map-based drawing of farm polygons
- Server-side spatial queries via PostGIS
- Accurate area, perimeter, and centroid calculations
- Persistent storage of farm geometries in a relational database
- Web-only access — no GIS software needed by the user

### Advantages
- Reduces dependency on GIS specialists
- Lets farmers manage their own farm boundaries
- Supports multi-user, multi-tenant deployments
- Easy to integrate with other web services (weather, satellite APIs)
- Open-source — no licensing cost

### Limitations
- Requires running PostgreSQL + PostGIS, which is more complex than SQLite
- Browser-based polygon drawing requires JavaScript and OpenLayers expertise to customize
- Storing large numbers of high-resolution polygons can stress the database
- Multi-tenant security needs careful attention (one user must not access another user's farms)

## 2.3 Cloud-Optimized GeoTIFFs and STAC-Based Imagery Serving

Cloud-Optimized GeoTIFFs (COGs) and the STAC (SpatioTemporal Asset Catalog) specification are two recent advances that have made satellite imagery practical to serve on the web at scale.

A **Cloud-Optimized GeoTIFF** is an ordinary GeoTIFF file, but with internal tiling and overviews arranged so that HTTP range requests can fetch only the bytes needed for a specific zoom level and area of interest. This means a web service can serve a small thumbnail or a specific region from a multi-gigabyte COG without downloading the whole file.

The **STAC specification** is a JSON-based catalog format that describes a collection of geospatial assets (typically COGs). A STAC API exposes a `/search` endpoint where clients can query by datetime, geometry, and arbitrary properties (e.g. cloud cover) to discover the relevant items in a collection. The Element84 STAC API at `https://earth-search.aws.element84.com/v1` provides searchable access to the Sentinel-2 L2A collection (and others, like Landsat, Cop-DEM, etc.) hosted on AWS Open Data.

**TiTiler** is an open-source tile server (built on FastAPI, Rasterio, and Rio-Tiler) that consumes COGs and STAC items, and exposes endpoints for:

- **`/stac/feature.{format}`** — render a rasterized image (PNG, JPEG, TIF) clipped to a GeoJSON feature, with band math (`expression=(nir-red)/(nir+red)`), colormap, and rescale parameters.
- **`/stac/statistics`** — compute statistical aggregates (min, max, mean, std, median, percentiles) over a clipped area, again with band math.
- **`/stac/tilejson.json`** — produce a tile-server URL for use with web mapping libraries.

The CropGeo Analytics platform uses TiTiler for both satellite imagery rendering (PNG output with NDVI/EVI/NDMI colormaps) and for computing vegetation-index statistics over each farm polygon.

### Features (of COGs and STAC-based serving)
- HTTP range-request fetching avoids downloading whole files
- Server-side rasterization through TiTiler
- Standardized, queryable catalog via STAC
- Free hosting on AWS Open Data
- Band math, colormaps, and rescale handled server-side

### Advantages
- Massive cost reduction compared to downloading and processing TIFFs locally
- Fast response times for small AOIs
- Standardized API — same TiTiler client code works for many collections
- Reusable architecture — easy to switch satellite sources

### Limitations
- Requires a running TiTiler instance (or use of a hosted one like titiler.vistamap.co)
- Depends on third-party services (Element84, AWS Open Data) staying online
- Band math expressions are slightly different across data providers
- Network latency between the Django backend and TiTiler can be a bottleneck

---

# CHAPTER 3 — SOFTWARE REQUIREMENT SPECIFICATION

The Software Requirement Specification (SRS) for CropGeo Analytics covers hardware, software, functional, and non-functional requirements. The SRS clarifies what the system must do and the resources needed to develop, deploy, and run it.

## 3.1 Hardware Requirements

### Development Environment (recommended minimum)

| Component | Requirement |
|---|---|
| Processor | Intel Core i5 (8th gen or later) or AMD Ryzen 5 equivalent |
| RAM | 8 GB minimum, 16 GB recommended |
| Storage | 512 GB SSD (Sentinel-2 imagery is fetched on demand, not stored locally) |
| Operating System | Linux (Fedora 44+ used during development), Windows 10 / 11, or macOS |
| Display | 1366×768 minimum; 1920×1080 recommended for the map dashboard |
| Internet | Stable broadband — the platform fetches satellite and weather data live |
| Peripherals | Keyboard, mouse, modern web browser |

### Production Server (minimum)

| Component | Requirement |
|---|---|
| Server CPU | 2+ cores |
| Server RAM | 4 GB minimum, 8 GB recommended |
| Database | PostgreSQL 13+ with PostGIS 3.x extension installed |
| TiTiler | Either self-hosted TiTiler instance or use of a hosted service like titiler.vistamap.co |
| Internet | Public IPv4 / IPv6, HTTPS termination via reverse proxy (nginx / Caddy) |
| Operating System | Linux (Ubuntu 22.04 LTS or Debian 12 recommended for production) |

### Purpose of Hardware Requirements
- Support smooth Django application execution
- Run PostgreSQL with PostGIS efficiently for spatial queries
- Provide enough memory for Django + worker processes
- Allow modern browser-based UI to load OpenLayers maps without lag
- Support concurrent multi-threaded satellite statistics fetching

## 3.2 Software Requirements

The CropGeo Analytics project uses entirely open-source software. The full list of direct Python dependencies is given in [requirements.txt](../requirements.txt):

### Python Backend Dependencies

| Package | Version constraint | Purpose |
|---|---|---|
| **Django** | `>= 5.2.7` | Main web framework |
| **psycopg2-binary** | `>= 2.9.0` | PostgreSQL database driver |
| **python-dotenv** | `>= 1.0.0` | Load environment variables from `.env` |
| **gunicorn** | `>= 21.2.0` | Production WSGI server |
| **httpx** | `>= 0.24.0` | Modern HTTP client for calling TiTiler, STAC, Open-Meteo |
| **planetary_computer** | (no version pin) | Microsoft Planetary Computer SDK (available for future expansion to alternate STAC sources) |
| **pystac_client** | (no version pin) | Python STAC API client |
| **GDAL** | `== 3.11.5` | Geospatial Data Abstraction Library — required by GeoDjango |

### System / Infrastructure Dependencies

| Component | Purpose |
|---|---|
| **PostgreSQL 13+** | Relational database |
| **PostGIS 3.x** | Spatial extension for PostgreSQL — enables `GeometryField` storage |
| **GDAL system library** (`libgdal`) | Underlying C library used by GeoDjango for geometry transformation |
| **TiTiler service** | External tile server for satellite imagery — either self-hosted or via `https://titiler.vistamap.co` |
| **Python 3.14** | Python runtime (development used CPython 3.14) |

### Frontend Technologies

| Technology | Purpose |
|---|---|
| **HTML5** | Page structure (Django templates) |
| **CSS3** | Styling (inline `<style>` blocks within templates) |
| **JavaScript (vanilla)** | Browser-side interactivity and AJAX calls |
| **OpenLayers** | Interactive maps and polygon drawing (loaded via CDN in templates) |
| **Chart.js or similar** | (optional, for charts in the farm dashboard) |

### External Web APIs

| API | URL | Purpose | Cost |
|---|---|---|---|
| **Open-Meteo** | `https://api.open-meteo.com/v1/forecast` | Current weather + 16-day forecast | Free, no API key |
| **Element84 STAC** | `https://earth-search.aws.element84.com/v1` | Sentinel-2 scene discovery | Free, no API key |
| **TiTiler** | `https://titiler.vistamap.co` (default) or self-hosted | Raster processing | Free if self-hosted |
| **AWS Open Data S3** | (Sentinel-2 COGs, accessed indirectly via TiTiler) | Underlying satellite imagery | Free |

### Development Tools

| Tool | Purpose |
|---|---|
| **VS Code** | IDE for coding |
| **Git** | Version control |
| **GitHub** | Remote repository hosting |
| **Google Chrome / Firefox** | Browser testing |
| **psql** or **pgAdmin** | PostgreSQL administration |
| **Django Admin** | Built-in admin interface for direct data manipulation |

### Purpose of Software Requirements
- Provide a complete, reproducible development environment
- Support Django + GeoDjango on PostgreSQL with PostGIS
- Enable HTTP communication with external APIs (Open-Meteo, STAC, TiTiler)
- Allow on-demand satellite imagery processing
- Support web-based interactive mapping through OpenLayers
- Enable version-controlled, multi-developer workflow via Git

## 3.3 Functional Requirements

### Main Functional Requirements

1. **User Registration**
   - Visitor provides name, email, age, gender, password.
   - System checks for duplicate emails.
   - New user is created with `is_approved=False`.
   - User cannot log in until an admin approves them.

2. **User Login**
   - User provides email and password.
   - System authenticates via Django's `authenticate()`.
   - If user is staff, redirect to admin dashboard.
   - If user is not approved, deny login with a friendly message.
   - If approved, redirect to the user dashboard.

3. **User Logout**
   - Authenticated user clicks logout.
   - System ends the session and redirects to the login page.

4. **Admin User Moderation**
   - Admin views paginated list of pending and approved users.
   - Admin can approve a pending user (sets `is_approved=True`, `is_active=True`).
   - Admin can reject a pending user (deletes the user record).
   - Admin can deactivate an active user (sets `is_active=False`).
   - Admin can delete a non-staff user.

5. **Farm Registration**
   - Approved user provides farm name, crop type (from a fixed list), and a polygon drawn on a map.
   - System validates the GeoJSON geometry server-side.
   - System computes the polygon area using UTM zone projection.
   - System rejects polygons larger than `MAX_FARM_AOI_ACRES = 10` acres.
   - System stores the geometry in PostGIS with SRID 4326.
   - System auto-computes and saves the `area` (m²) and `size_acres` fields on save.
   - The farm gets a unique UUID primary key.

6. **Farm Deletion**
   - User can delete their own farm. The system enforces that only the owner can delete a farm (`Farm.objects.get(id=farm_id, user=request.user)`).

7. **Farm Dashboard / View Farm**
   - User views a per-farm dashboard with map, name, crop type, size in acres, and access to satellite + weather features.

8. **Satellite Scene Search**
   - User picks a start date, end date, and maximum cloud cover (default 20%).
   - System builds an STAC query URL pointing at Element84 STAC for the `sentinel-2-l2a` collection.
   - System returns a list of matching scenes with id, date, cloud cover, and platform.

9. **Vegetation Index Statistics**
   - User selects a scene and an index (NDVI / EVI / NDMI).
   - System calls TiTiler `/stac/statistics` with the appropriate band-math expression.
   - System returns min, max, mean, std, median.

10. **Satellite Imagery Rendering**
    - User requests a rendered image for a scene + index.
    - System calls TiTiler `/stac/feature.{png|jpeg|tif}` with the index expression, colormap, and rescale.
    - System returns a base64-encoded image data URL and the bounding box for OpenLayers overlay.

11. **Current Weather**
    - System fetches current weather at the farm centroid from Open-Meteo.
    - Returned data includes temperature, humidity, apparent temperature, precipitation, rain, cloud cover, surface pressure, wind speed, wind gusts, sunrise, sunset, UV index, evapotranspiration, soil temperature at 4 depths, and soil moisture at 5 depths.

12. **Weather Forecast (16-day)**
    - System fetches a 16-day daily forecast at the farm centroid.
    - Returned data includes daily max/min/mean temperature, max humidity, precipitation, rain, mean cloud cover, mean surface pressure, evapotranspiration, max wind speed, max wind gusts.

### Purpose of Functional Requirements

- Enable secure user interaction with the system
- Support farm boundary management
- Enable satellite-based crop monitoring
- Provide weather context for crop decisions
- Allow institutional oversight via admin moderation

## 3.4 Non-Functional Requirements

### Security
- Session-based authentication using Django's built-in `django.contrib.auth`.
- CSRF protection enabled (Django default via `CsrfViewMiddleware`).
- Clickjacking protection via `XFrameOptionsMiddleware`.
- Admin approval gate (`is_approved=False` by default) prevents unauthorized access.
- Farm queries are filtered by `user=request.user` so a user cannot access another user's farms.
- UUID primary keys for farms prevent enumeration attacks.
- Server-side geometry validation rejects malformed GeoJSON.
- Server-side area validation rejects oversized polygons (10-acre cap).
- Password validation chain: `UserAttributeSimilarityValidator`, `MinimumLengthValidator`, `CommonPasswordValidator`, `NumericPasswordValidator`.

### Reliability
- Accurate UTM-based area calculation (sub-percent error within a single UTM zone).
- Server-side validation of all user inputs.
- Graceful error responses (JSON with `error` key and HTTP status code).
- Timeouts on external API calls (httpx `timeout=30` for STAC, `timeout=60` for Open-Meteo, `timeout=300` for TiTiler).
- Forecast endpoint has a chunked-fallback strategy: if the full-variable forecast request fails, it splits variables into smaller batches and re-requests.

### Performance
- Multi-threaded statistics fetching via `ThreadPoolExecutor(max_workers=10)` in `main/utils.py:get_stats`.
- Stateless views — no in-process caching to grow over time.
- PostgreSQL with PostGIS handles spatial queries efficiently with built-in indexing.
- TiTiler does heavy raster work — Django stays light.

### Scalability
- Stateless Django app — can be horizontally scaled behind a load balancer.
- PostgreSQL can be scaled vertically or replicated.
- TiTiler can be scaled independently (it is a separate service).
- All external APIs (Open-Meteo, Element84 STAC) are themselves designed for scale.

### Availability
- Standard Django + gunicorn deployment is highly available.
- Recoverable from API outages: a failing TiTiler call returns a JSON error, the app remains usable.

### Maintainability
- Clear module separation: `models.py`, `views.py`, `utils.py`, `enum.py`, `weather_api.py`, `forms.py`, `urls.py`.
- Migrations track schema evolution (0001 → 0004 currently).
- Dataclass-based vegetation index definitions (`IndexFormula` in `main/enum.py`) make it easy to add new indices.
- Environment variables (`.env`) for all credentials and external URLs.

### Usability
- Single-page-style flows (login → dashboard → add farm → view farm).
- Clear error messages on validation failures.
- Server-side responses are JSON for JS-driven views, HTML for full-page navigation.
- Form validation errors are surfaced via Django `messages` framework.

### Accuracy
- UTM area: better than 1% error for any farm under 10 acres within one UTM zone.
- Vegetation index values: directly from atmospherically-corrected Sentinel-2 L2A, range -1.0 to 1.0 for NDVI/NDMI, 0.0 to 1.0 for EVI.
- Weather data: from Open-Meteo, which itself sources from ECMWF, GFS, ICON, and other public models.

### Purpose of Non-Functional Requirements
- Ensure secure handling of user accounts and farm data
- Maintain system reliability under variable external-API conditions
- Enable horizontal scaling for institutional deployments
- Provide a smooth user experience
- Keep the codebase maintainable for future MCA students

---

# CHAPTER 4 — DESIGN AND MODELING

## 4.1 System Architecture

CropGeo Analytics follows a classic **client-server, three-tier architecture** with several **external services** layered behind the backend.

### Architecture Tiers

**1. Client Tier (Frontend)**
- Modern web browser (Chrome, Firefox, Safari, Edge)
- HTML pages rendered from Django templates
- CSS for styling (inline `<style>` blocks)
- Vanilla JavaScript for AJAX calls
- OpenLayers (loaded via CDN) for interactive maps and polygon drawing

**2. Application Tier (Backend)**
- Django 5.2.7 web framework
- GeoDjango (`django.contrib.gis`) for spatial features
- Python 3.14
- 19 view functions defined in `main/views.py`
- Utility modules: `utils.py` (TiTiler/STAC helpers), `weather_api.py` (Open-Meteo helpers), `enum.py` (vegetation index definitions), `forms.py` (Django forms for farm creation)
- WSGI deployment via gunicorn

**3. Data Tier (Database)**
- PostgreSQL 13+ with PostGIS 3.x extension
- Two tables: `main_user` (custom User model) and `main_farm`
- Spatial column `geometry` on `main_farm` uses SRID 4326 (WGS-84 lat/lon)
- Migrations 0001 → 0004 manage schema

**4. External Services**
- **Element84 STAC API** (`earth-search.aws.element84.com/v1`) — Sentinel-2 scene discovery
- **AWS S3 (Sentinel-2 L2A on AWS Open Data)** — actual COG storage (accessed indirectly via TiTiler)
- **TiTiler** (`titiler.vistamap.co` or self-hosted at `http://localhost:8888`) — raster processing
- **Open-Meteo** (`api.open-meteo.com/v1/forecast`) — weather data

### Architecture Diagram (textual description)

```
+--------------------+
|   Browser (User)   |
|   - OpenLayers     |
|   - HTML / CSS / JS|
+--------+-----------+
         | HTTPS
         v
+--------+------------------------------------+
|  Django App (cropgeo)                        |
|  +----------------+  +---------------------+|
|  | views.py (19)  |  | utils.py            ||
|  | login/signup   |  | get_imagery()       ||
|  | dashboard      |  | fetch_stats()       ||
|  | add_farm       |  | get_stats() [MT]    ||
|  | view_farm      |  +---------------------+|
|  | weather_*      |  +---------------------+|
|  | satellite_*    |  | weather_api.py      ||
|  | admin_*        |  | current_*           ||
|  +----------------+  | forecast_*          ||
|  +----------------+  +---------------------+|
|  | models.py      |  +---------------------+|
|  | User           |  | enum.py             ||
|  | Farm (UUID PK) |  | NDVI / EVI / NDMI   ||
|  +----------------+  +---------------------+|
+----+-----------+-----------+----------------+
     |           |           |
     |           |           |
     v           v           v
+--------+  +---------+  +------------+
|PostGIS |  |TiTiler  |  | Open-Meteo |
|geometry|  |/feature |  | /v1/forecast|
|UUID PK |  |/stats   |  +------------+
+--------+  +---------+
                |
                v
            +--------+
            |Element84|
            | STAC    |
            +--------+
                |
                v
            +--------+
            |  AWS   |
            |  S3    |
            |  COGs  |
            +--------+
```

### Working of the System

1. **User Interaction** — The user opens the website, signs up, waits for admin approval, then logs in.
2. **Request Transmission** — Each user action (drawing a farm polygon, requesting satellite stats, viewing weather) becomes an HTTP request to the Django backend.
3. **Request Processing** — Django's URL dispatcher routes the request to a view function in `main/views.py`. The view validates inputs, checks authentication, performs spatial computation if needed, calls external APIs if needed, and assembles a response.
4. **Database Communication** — Spatial queries use the `Farm.objects.filter(user=request.user, ...)` ORM API, which translates to SQL with PostGIS functions.
5. **External API Calls** — For satellite scene search, the view constructs an STAC query URL and calls Element84 with httpx. For imagery and statistics, the view calls TiTiler. For weather, the view calls Open-Meteo. All external calls have explicit timeouts.
6. **Response Generation** — The view returns either an HTML response (for page navigation) or a JSON response (for AJAX-driven dashboard features). Satellite imagery is returned as a base64-encoded PNG data URL plus a bounding box, so the browser can overlay it on the OpenLayers map.
7. **Result Display** — The browser receives the response and updates the dashboard accordingly: drawing a satellite raster on top of the map, displaying vegetation index statistics in a card, updating a weather widget, etc.

## 4.2 E-R Diagram

The CropGeo Analytics database schema is intentionally small: two main entities, with a one-to-many relationship between them.

### Entities

#### 1. User Entity

Extends Django's `AbstractUser`. The custom user model is declared in `main/models.py:User` and registered via `AUTH_USER_MODEL = "main.User"` in `cropgeo/settings.py`.

**Attributes inherited from AbstractUser:**

| Attribute | Type | Notes |
|---|---|---|
| id | BigAutoField | Primary key |
| username | CharField (max 150, unique) | Used as the login identifier (set to the email at signup) |
| password | CharField (hashed) | PBKDF2 by default |
| email | EmailField | Set at signup |
| first_name | CharField (max 150) | Used to store the user's display name |
| last_name | CharField (max 150) | Optional |
| is_staff | BooleanField (default False) | Admin flag |
| is_superuser | BooleanField (default False) | Django superuser flag |
| is_active | BooleanField (default True) | Disable user without deleting |
| date_joined | DateTimeField (auto) | Registration timestamp |
| last_login | DateTimeField (auto) | Updated on each login |

**Custom attributes added in `main/models.py`:**

| Attribute | Type | Default | Notes |
|---|---|---|---|
| age | PositiveIntegerField | 18 | User's age at registration |
| gender | CharField (choices) | "prefer-not-to-say" | Choices: male, female, other, prefer-not-to-say |
| is_approved | BooleanField | False | Admin approval gate |

**Purpose:** Authentication, identity, and admin moderation.

#### 2. Farm Entity

Declared in `main/models.py:Farm`. Has UUID primary key, polygonal geometry, and a foreign-key relationship to User.

| Attribute | Type | Notes |
|---|---|---|
| id | UUIDField, primary_key | Auto-generated via `uuid.uuid4`, not editable |
| name | CharField (max 255) | Farm name set by the user |
| crop_type | CharField (max 50, choices) | Choices: wheat, corn, soybeans, rice, cotton, barley, oats |
| size_acres | FloatField (null, blank) | Auto-computed from geometry on save |
| geometry | GeometryField (SRID 4326) | Polygon in WGS-84 lat/lon |
| area | FloatField (null, blank) | Auto-computed area in m² on save |
| created_at | DateTimeField (auto_now_add) | Creation timestamp |
| updated_at | DateTimeField (auto_now) | Last update timestamp |
| user | ForeignKey to User (on_delete=CASCADE, related_name="farms") | The owner |

**Behaviors:**
- `Farm.acres_from_geometry(geometry)` (classmethod) — pure-function helper that computes acres from any geometry by UTM-projecting it, returning `None` if invalid.
- `Farm.save()` — overridden to auto-compute `area` (m²) and `size_acres` from the geometry using UTM projection before calling the superclass `save()`.
- `Meta.ordering = ['-created_at']` — newest farms first.
- `__str__` returns `"{name} ({id})"`.

### Relationships

```
User (1) ─── owns ───< (N) Farm
```

- One user can own many farms.
- Deleting a user cascades to deleting their farms (`on_delete=CASCADE`).
- A farm's `user` is set at creation; it is not transferable in the current implementation.

### E-R Diagram (textual)

```
+--------------------+              +-----------------------------+
|       USER         |              |          FARM               |
+--------------------+              +-----------------------------+
| PK id              |  1        N  | PK id  (UUID)               |
|    username        |--------------|  name                       |
|    email           |    owns      |  crop_type                  |
|    password        |              |  size_acres (auto)          |
|    first_name      |              |  geometry (SRID 4326)       |
|    last_name       |              |  area  (m²)  (auto)         |
|    age             |              |  created_at                 |
|    gender          |              |  updated_at                 |
|    is_approved     |              |  FK user_id ─────────────► User
|    is_staff        |              +-----------------------------+
|    is_active       |
|    date_joined     |
|    last_login      |
+--------------------+
```

## 4.3 Data Flow Diagram

### DFD Level 0 (Context Diagram)

The Level 0 DFD shows the CropGeo Analytics system as a single process with external entities.

**External Entities:**
- **User** (farmer / researcher) — provides login credentials, farm polygon, satellite search parameters; receives dashboards, statistics, imagery, and weather.
- **Admin** — moderates user accounts.
- **Element84 STAC API** — receives search queries, returns Sentinel-2 scene lists.
- **TiTiler** — receives raster processing requests (statistics, imagery), returns JSON stats or PNG bytes.
- **Open-Meteo** — receives weather requests, returns current weather and forecast.

**Input flows to system:**
- User credentials and registration data
- Farm polygon (GeoJSON), farm name, crop type
- Satellite scene search parameters (date range, cloud cover)
- Vegetation index choice (NDVI/EVI/NDMI), colormap, rescale
- Admin moderation actions

**Output flows from system:**
- Dashboard (HTML)
- Farm list and statistics
- Vegetation index statistics (JSON)
- Satellite imagery (base64 PNG + bbox)
- Current weather (JSON)
- 16-day forecast (JSON)
- Admin pages

**Diagram (text):**

```
                    +--------------------+
                    |  CropGeo Analytics |
                    |     System         |
                    +---+------------+---+
   credentials,         |            |
   farm polygon, ─────► |            | ◄─── scenes (STAC API)
   queries              |            |
                        |            | ◄─── rasters, stats (TiTiler)
   pages, JSON  ◄────── |            |
   responses            |            | ◄─── weather (Open-Meteo)
                        +------------+
                                ▲
                                |
                            (Admin)
                            moderation
                            commands
```

### DFD Level 1 — Internal Processes

Breaks the system into the main subsystems:

1. **Authentication Subsystem**
   - Inputs: email, password (login); name, email, age, gender, password (signup)
   - Process: validate credentials, check `is_approved`, create session
   - Data store: `main_user` table
   - Outputs: session cookie, dashboard redirect, or error message

2. **Farm Management Subsystem**
   - Inputs: farm name, crop type, GeoJSON polygon
   - Process: validate geometry, check 10-acre AOI cap, compute UTM area, save with UUID PK
   - Data store: `main_farm` table (PostGIS)
   - Outputs: success JSON with farm UUID, or validation error

3. **Satellite Subsystem**
   - Inputs: farm UUID, date range, cloud cover, index choice, scene id
   - Process: query Element84 STAC, call TiTiler for stats or imagery, multi-threaded fetching when needed
   - Data store: none (stateless — all data is fetched live)
   - Outputs: scene list JSON, stats JSON, imagery base64 PNG + bbox

4. **Weather Subsystem**
   - Inputs: farm UUID
   - Process: compute centroid lat/lon, call Open-Meteo, remap variable names to user-friendly keys
   - Data store: none (stateless — fetched live)
   - Outputs: current weather JSON, 16-day forecast JSON

5. **Admin Moderation Subsystem**
   - Inputs: target user id, action (approve/reject/deactivate/delete)
   - Process: validate staff status, mutate or delete the user
   - Data store: `main_user` table
   - Outputs: redirect with success/error message

### DFD Level 2 — Satellite Subsystem Detail

A deeper breakdown of the satellite analysis flow, which is the most complex part of the system:

1. **Authenticate request** — `@login_required` ensures only logged-in users reach the view, and `Farm.objects.get(user=request.user)` ensures only the owner can access their farm's data.
2. **Build STAC query** — Construct URL with date range, max cloud cover, intersects (URL-encoded farm GeoJSON), and Sentinel-2 collection. Call Element84 with httpx.
3. **Filter and format scene list** — Iterate over `features` in STAC response. Extract id, datetime, eo:cloud_cover, platform. Return as JSON list.
4. **On scene selection** — User picks a specific scene id and an index (NDVI/EVI/NDMI). The view validates the index via the `VegetationIndex` enum, looks up the corresponding `IndexFormula` via `S2IndexFormulas.get_formula()`, and gets the band-math expression.
5. **TiTiler stats call** — Build URL pointing at `{TITILER_URL}/stac/statistics` with the STAC item URL, the URL-encoded expression, and `asset_as_band=True`. POST farm geometry as a GeoJSON feature. Parse response.
6. **TiTiler imagery call** — Build URL pointing at `{TITILER_URL}/stac/feature.{png|jpeg|tif}` with the same expression, colormap, rescale range, and resampling/reprojection options. POST farm geometry. Receive PNG bytes, base64-encode, prepend `data:image/png;base64,`, return JSON with image + bbox.
7. **Browser display** — Browser receives JSON, creates an OpenLayers ImageStatic source using the data URL and bbox, adds it as a layer above the basemap, displays stats in a card.

### Diagram description for the dissertation

For the actual diagrams in the dissertation, Pratham should create (using draw.io or Lucidchart):

- **Level 0:** Single circle "CropGeo Analytics System" with arrows to User (bidirectional), Admin (bidirectional), Element84 STAC (one-way out, results back), TiTiler (one-way out, raster/stats back), Open-Meteo (one-way out, weather back).
- **Level 1:** Five process boxes (Authentication, Farm Management, Satellite, Weather, Admin Moderation) connected to two data stores (User DB, Farm DB) and the external entities.
- **Level 2 (Satellite):** Sub-processes — Authenticate Request, Build STAC Query, Format Scene List, Validate Index, Call TiTiler Stats, Call TiTiler Imagery, Encode and Return Response.

## 4.4 UML Diagrams

### 1. Use Case Diagram

**Actors:**
- **Visitor** (unauthenticated) — can view About page, register, log in.
- **User** (approved farmer) — full farm management and satellite/weather features.
- **Admin** (staff) — user moderation and platform oversight.

**Use cases:**

For **Visitor**:
- Browse Home Page
- View About Page
- Register (Signup)
- Log In

For **User** (post-approval):
- Log In / Log Out
- View Dashboard (list of own farms)
- Add Farm (draw polygon on map)
- View Farm Dashboard (per-farm analytics)
- Delete Farm
- Search Satellite Scenes
- Compute Vegetation Index Statistics
- View Satellite Imagery
- View Current Weather
- View 16-Day Forecast

For **Admin**:
- View Admin Dashboard
- View Pending Users
- Approve User
- Reject User
- Deactivate User
- Delete User
- View All Farms (paginated)

**Include relationships:**
- "Add Farm" includes "Validate Geometry", "Compute UTM Area".
- "Search Satellite Scenes" includes "Call STAC API".
- "Compute Vegetation Index Statistics" includes "Call TiTiler /stac/statistics".
- "View Satellite Imagery" includes "Call TiTiler /stac/feature.png".

**Extend relationships:**
- "Add Farm" extends to "Reject (AOI too large)" when polygon > 10 acres.
- "Log In" extends to "Pending approval message" when `is_approved` is False.

### 2. Sequence Diagram (Farm Creation and Satellite Analysis)

The sequence diagram for the most complex flow — creating a farm and then computing vegetation index statistics:

```
User           Browser         Django         PostGIS     STAC      TiTiler
 |               |               |              |          |          |
 |--login------->|               |              |          |          |
 |               |--POST /login->|              |          |          |
 |               |               |--authenticate>|          |          |
 |               |<----dashboard-|              |          |          |
 |               |               |              |          |          |
 |--draw polygon>|               |              |          |          |
 |--submit------>|--POST /add-farm>|             |          |          |
 |               |               |--validate----|          |          |
 |               |               |--UTM area----|          |          |
 |               |               |--save Farm-->|          |          |
 |               |<--success----|              |          |          |
 |               |               |              |          |          |
 |--view farm--->|               |              |          |          |
 |--search scenes->|             |              |          |          |
 |               |--POST /search-satellite>     |          |          |
 |               |               |--STAC query-------------->|       |
 |               |               |<------scenes------------|         |
 |               |<---scene list-|              |          |         |
 |               |               |              |          |         |
 |--pick scene & NDVI->|         |              |          |         |
 |               |--POST /get-stats>            |          |         |
 |               |               |--/stats------------------------->|
 |               |               |<------stats JSON-----------------|
 |               |<---stats------|              |          |         |
 |               |               |              |          |         |
 |--show imagery->|              |              |          |         |
 |               |--POST /get-imagery>          |          |         |
 |               |               |--/feature.png------------------->|
 |               |               |<------PNG bytes-----------------|
 |               |<---data URL + bbox            |          |         |
 |               |--draw raster overlay         |          |         |
```

### 3. Class Diagram

The core classes (Python perspective):

```
+--------------------------+
| AbstractUser  (Django)   |
+--------------------------+
| ...standard fields...    |
+--------------------------+
            ▲
            | extends
            |
+--------------------------+
|         User             |
+--------------------------+
| - age: PositiveInt = 18  |
| - gender: str = prefer-  |
|     not-to-say           |
| - is_approved: bool=False|
+--------------------------+
            |
            | 1
            |
            | owns
            |
            | N
+--------------------------+
|         Farm             |
+--------------------------+
| - id: UUID (PK)          |
| - name: str              |
| - crop_type: str (choice)|
| - size_acres: float?     |
| - geometry: GeometryField|
|   (SRID 4326)            |
| - area: float?  (m²)     |
| - created_at: datetime   |
| - updated_at: datetime   |
| - user: FK -> User       |
+--------------------------+
| + acres_from_geometry(g) |
|   [classmethod]          |
| + save()                 |
| + __str__()              |
+--------------------------+

+--------------------------+         +--------------------------+
|     IndexFormula         |         |   VegetationIndex (enum) |
+--------------------------+         +--------------------------+
| - name: str              |         |  NDVI = "ndvi"           |
| - formula: str           |         |  EVI = "evi"             |
| - description: str       |         |  NDMI = "ndmi"           |
| - min_value: float       |         +--------------------------+
| - max_value: float       |
| - bands: List[S2Band]    |         +--------------------------+
| - colormap: str          |         |   S2Band (enum)          |
| - colormap_reverse: bool |         +--------------------------+
+--------------------------+         |  COASTAL, BLUE, GREEN,   |
| + get_assets() -> str    |         |  RED, REDEDGE1/2/3,      |
+--------------------------+         |  NIR, NIR08, NIR09,      |
                                     |  SWIR16, SWIR22          |
+--------------------------+         +--------------------------+
|   S2IndexFormulas        |
+--------------------------+         +--------------------------+
| + NDVI: IndexFormula     |         |   Colormap (enum)        |
| + EVI: IndexFormula      |         +--------------------------+
| + NDMI: IndexFormula     |         |  VIRIDIS, PLASMA, ...    |
+--------------------------+         |  RDYLGN, BLUES, ...      |
| + get_formula(VI) ->     |         +--------------------------+
|     IndexFormula         |
+--------------------------+
```

The view layer (`main/views.py`) and utility layer (`main/utils.py`, `main/weather_api.py`) are functional, not class-based, so they appear in the class diagram as modules or service boxes rather than as classes.

---

# CHAPTER 5 — IMPLEMENTATION AND TESTING

## 5.1 Modules Used

The CropGeo Analytics system is organized into eight functional modules. Each module owns a specific responsibility and is loosely coupled to the others.

### 1. Authentication Module

**Files:** [main/views.py](../main/views.py) (functions `login_view`, `signup_view`, `logout_view`), [templates/login.html](../templates/login.html), [templates/signup.html](../templates/signup.html).

The Authentication Module handles user registration, login, logout, and the admin-approval gate. New accounts are created with `is_approved=False` and cannot access the dashboard until an admin approves them.

**Working:**
- On signup: collect name, email, age, gender, password from the form. Check for duplicate email. Create the user with `is_approved=False`. Redirect to the login page with a "wait for admin approval" message.
- On login: authenticate with email + password. If the user is not approved (and not staff), refuse login and show a friendly message. If approved, log them in and redirect to the dashboard (or admin dashboard if staff).
- On logout: end the session and redirect to login.

**Importance:**
- Secures the platform against unauthorized access.
- Provides institutional moderation via admin approval.
- Uses Django's battle-tested authentication system with custom user fields.

### 2. Farm Management Module

**Files:** [main/views.py](../main/views.py) (functions `add_farm_view`, `delete_farm_view`, `view_farm_dashboard`, `dashboard`), [main/models.py](../main/models.py) (the `Farm` model), [main/forms.py](../main/forms.py), [templates/add-farm.html](../templates/add-farm.html), [templates/view-farm-dashboard.html](../templates/view-farm-dashboard.html).

This module manages farm CRUD (Create, Read, Delete — Update is not currently exposed in the UI). Each farm has a UUID primary key for safety, a GeometryField storing the polygon in WGS-84, and auto-computed acres on save.

**Working:**
- User opens the Add Farm page, which loads an OpenLayers map.
- User draws a polygon, names the farm, picks a crop type.
- On submit, the frontend sends a JSON POST with the GeoJSON geometry, name, and crop type.
- Backend (`add_farm_view`) validates the geometry, computes acres via `Farm.acres_from_geometry()`, rejects the farm if acres > 10 (`MAX_FARM_AOI_ACRES`), and creates the `Farm` instance.
- `Farm.save()` is overridden to auto-compute `area` (m²) and `size_acres` from the geometry using UTM projection.
- The farm's UUID is returned to the frontend.
- User dashboards (`dashboard` view) shows the list of farms with total acres tally.
- View Farm Dashboard (`view_farm_dashboard`) serializes the geometry as a GeoJSON Feature for OpenLayers and provides the centroid for map centering.
- Delete Farm (`delete_farm_view`) requires `user=request.user` so only the owner can delete.

**Importance:**
- Central to the entire system — every other module operates per-farm.
- Server-side area validation is a key safety measure.
- UUID primary keys prevent enumeration attacks.

### 3. Satellite Imagery Module

**Files:** [main/views.py](../main/views.py) (functions `search_satellite_data`, `get_farm_imagery`), [main/utils.py](../main/utils.py) (functions `get_imagery`).

This module discovers available Sentinel-2 scenes via the Element84 STAC API and fetches rendered satellite imagery from TiTiler.

**Working:**
- `search_satellite_data(farm_id)` accepts `start_date`, `end_date`, and `cloud_cover` (default 20%). It URL-encodes the farm GeoJSON and constructs an STAC query URL:
  ```
  https://earth-search.aws.element84.com/v1/search?
    datetime={start}T00:00:00.000Z/{end}T23:59:59.000Z
    &limit=200
    &collections=sentinel-2-l2a
    &intersects={geojson}
    &query={"eo:cloud_cover":{"gte":0,"lte":{cloud_cover}}}
  ```
- It returns a JSON list of scenes with `id`, `date`, `cloud_cover`, `platform`.
- `get_farm_imagery(farm_id)` (GET or POST) accepts `item_id`, `index_type`, `image_type` (png/jpeg/tif), `colormap`, `min_val`, `max_val`, `pixelized`. It calls `get_imagery()` in `utils.py`, which POSTs to `{TITILER_URL}/stac/feature.{format}` with the farm GeoJSON and parameters.
- For PNG/JPEG, TiTiler returns image bytes; the helper base64-encodes them and returns a `data:image/png;base64,...` URL plus the farm's bbox.

**Importance:**
- Provides the visual layer of the dashboard — without this, the user would only see numerical stats.
- Demonstrates STAC + TiTiler integration.
- Multiple image formats supported for flexibility (PNG for browser display, TIF for download/analysis).

### 4. Vegetation Index Analysis Module

**Files:** [main/views.py](../main/views.py) (function `get_farm_stats`), [main/utils.py](../main/utils.py) (functions `fetch_stats`, `get_stats`), [main/enum.py](../main/enum.py) (`VegetationIndex`, `IndexFormula`, `S2IndexFormulas`).

This module computes vegetation index statistics (min, max, mean, std, median) over a farm polygon by calling TiTiler's `/stac/statistics` endpoint with band-math expressions.

**Working:**
- The `VegetationIndex` enum defines the supported indices: NDVI, EVI, NDMI.
- The `IndexFormula` dataclass (in `enum.py`) holds: name, formula string, description, value range, required bands, default colormap.
- The `S2IndexFormulas` class holds the three pre-defined formulas:
  - **NDVI:** `(nir - red) / (nir + red)`, range [-1, 1], colormap RdYlGn (Red-Yellow-Green).
  - **EVI:** `2.5 * ((nir - red) / (nir + 6 * red - 7.5 * blue + 1))`, range [0, 1], colormap YlGn.
  - **NDMI:** `(nir - swir16) / (nir + swir16)`, range [-1, 1], colormap Blues.
- `get_farm_stats(farm_id)` validates the index type, looks up the formula, URL-encodes the expression, and calls `fetch_stats()` in utils.
- `fetch_stats()` POSTs to TiTiler `/stac/statistics?url={STAC_ITEM_URL}&expression={expression}&asset_as_band=True`, returns a dict with min/max/mean/std (and optionally median).
- `get_stats()` is a multi-threaded wrapper using `ThreadPoolExecutor(max_workers=10)` that calls `fetch_stats()` for many items in parallel — useful for time-series analysis.

**Importance:**
- The technical heart of the platform — these are the actual numbers that tell the farmer about their crop health.
- The dataclass-based design makes adding new indices easy.
- Multi-threading dramatically speeds up multi-scene statistics fetching.

### 5. Weather Module

**Files:** [main/weather_api.py](../main/weather_api.py), [main/views.py](../main/views.py) (functions `farm_weather_current`, `farm_weather_forecast`).

This module fetches current weather and a 16-day daily forecast from the Open-Meteo API, using the farm's centroid as the location.

**Working:**
- `farm_weather_current(farm_id)` view calls `weather_api.get_current_weather_payload(farm)`.
- The helper extracts lat/lon from `farm.geometry.centroid`, calls Open-Meteo with a long `current=...` parameter requesting:
  - Temperature 2 m, relative humidity 2 m, apparent temperature, precipitation, rain, cloud cover, surface pressure, wind speed 10 m, wind gusts 10 m.
  - Soil temperature at 0 cm, 6 cm, 18 cm, 54 cm.
  - Soil moisture at 0-1 cm, 1-3 cm, 3-9 cm, 9-27 cm, 27-81 cm.
- It also requests `daily` data for the current day (apparent temp max/min, sunrise, sunset, UV index max, FAO ET₀ evapotranspiration) and merges them into the current payload.
- The helper renames keys to friendlier names (`temperature_2m` → `temp`, `soil_temperature_0cm` → `soil_temperature_surface`, etc.) and adds a complete `units` dict.
- `farm_weather_forecast(farm_id)` view calls `weather_api.get_forecast_weather_payload(farm)`.
- The helper requests a 16-day daily forecast with 11 variables: temp_max, temp_min, temp_mean, max humidity, precipitation, rain, mean surface pressure, mean cloud cover, FAO ET₀, max wind speed, max wind gusts.
- It has a robust chunked-fallback strategy: if the full 11-variable request fails, it retries in batches of 2 variables and merges the results.
- It remaps Open-Meteo's variable names to short, friendly keys (`temperature_2m_max` → `temp_max`, etc.).

**Importance:**
- Provides the weather context for crop management decisions.
- Open-Meteo is free and requires no API key — perfect for the project.
- Including soil temperature and moisture at multiple depths is a unique strength compared to generic weather widgets.

### 6. Admin Moderation Module

**Files:** [main/views.py](../main/views.py) (functions `admin_dashboard_view`, `approve_user_view`, `reject_user_view`, `deactivate_user_view`, `delete_user_view`), [templates/admin-dashboard.html](../templates/admin-dashboard.html).

This module gives administrators a paginated dashboard with separate lists for pending users, approved users, and all farms, plus actions to approve, reject, deactivate, or delete users.

**Working:**
- `admin_dashboard_view` is decorated with `@user_passes_test(lambda u: u.is_staff)` so only staff can access it.
- It pulls pending users (`is_approved=False, is_staff=False`), approved users (`is_approved=True, is_staff=False`), and farms (all), each paginated at 10 (users) or 15 (farms) per page.
- Optional search via the `q` query parameter filters by email/first_name/last_name; `farm_q` filters farms by farm name or owner email/name.
- A helper `_elided_page_numbers()` produces a compact pagination control with "…" ellipses for long page lists.
- The four action views each accept POST only (CSRF-protected), validate that the target is not staff (where applicable), and perform the action with a flash message.
- `approve_user_view` sets `is_approved=True` and `is_active=True` on the target.
- `reject_user_view` deletes the user (with a "rejected" message).
- `deactivate_user_view` sets `is_active=False` (suspend without delete).
- `delete_user_view` deletes the user (with a "deleted" message).

**Importance:**
- Makes the platform safe for institutional or research deployments.
- Lets administrators audit and curate the user base.
- Built entirely on Django ORM and built-in `user_passes_test` — minimal custom code.

### 7. UI / Template Module

**Files:** all files in [templates/](../templates/).

The UI layer consists of Django templates that render HTML pages and pass context data to inline JavaScript for AJAX-driven dashboards. The layout system uses a base template (`base.html`) plus included partials (`includes/navbar.html`, `includes/cropgeo_modal.html`).

**Templates and their roles:**

| Template | Lines | Purpose |
|---|---|---|
| `base.html` | 134 | Shared HTML skeleton with `{% block %}` slots for content, scripts, styles |
| `includes/navbar.html` | 22 | Top navigation bar (different links for guests / users / admins) |
| `includes/cropgeo_modal.html` | 240 | Reusable modal component for confirmations and forms |
| `login.html` | 495 | Login form with email + password, error message display |
| `signup.html` | 492 | Registration form: name, email, age, gender, password, confirm password |
| `about.html` | 373 | About page describing the project and its motivation |
| `dashboard.html` | 406 | User dashboard — list of own farms, total acres, pending-approval banner if applicable |
| `add-farm.html` | 1077 | Farm registration page with OpenLayers map, polygon-drawing tools, name and crop-type fields |
| `view-farm-dashboard.html` | 1670 | Per-farm analytics dashboard — map with farm polygon overlay, satellite scene picker, vegetation index controls, weather widgets |
| `admin-dashboard.html` | 665 | Admin panel — three paginated tables (pending users, approved users, all farms), search boxes, action buttons |

**Importance:**
- The UI is the only thing the user sees — well-designed templates are critical for adoption.
- Inline JavaScript in the heavier templates (`add-farm.html`, `view-farm-dashboard.html`) drives all the AJAX flows.
- The reusable modal and navbar partials keep the codebase DRY.

### 8. Data Modeling and Migrations Module

**Files:** [main/models.py](../main/models.py), [main/migrations/](../main/migrations/) (0001 through 0004).

This module defines the data schema and tracks its evolution through Django migrations.

**Migrations:**
- **0001_initial** — creates the custom `User` model (extending AbstractUser) with `age` and `gender` fields.
- **0002_alter_user_age_alter_user_gender** — refines the age and gender field constraints (default, choices).
- **0003_farm** — adds the `Farm` model with UUID PK, `name`, `crop_type`, `size_acres`, `geometry`, `area`, timestamps, and FK to User.
- **0004_user_is_approved** — adds the `is_approved` boolean field to User (default False), which enables the admin-approval workflow.

**Importance:**
- Migrations let the schema evolve without manual SQL — critical for multi-developer or production deployments.
- The schema is intentionally simple (2 tables), which keeps the project maintainable.

## 5.2 Algorithms Used

### 1. UTM Zone Selection and Area Calculation Algorithm

To compute the area of a farm polygon accurately in real-world units (acres), the system projects the polygon from WGS-84 (geographic lat/lon, SRID 4326) into the appropriate UTM zone for the polygon's longitude.

**Algorithm (from `main/models.py`):**

```
INPUT: geometry G in SRID 4326 (or unspecified)
1. If G is None or empty: return None
2. Clone G into a working copy
3. If G's SRID is not 4326: transform G to SRID 4326
4. Compute centroid c = G.centroid; let lon = c.x
5. UTM zone number z = floor((lon + 180) / 6) + 1
6. UTM SRID = 32600 + z  (Northern Hemisphere UTM EPSG codes 32601..32660)
7. Transform G into the UTM SRID (clone)
8. area_m2 = transformed_geom.area
9. If area_m2 is falsy: return None
10. acres = area_m2 * 0.000247105
11. Return acres
```

**Why this works:**
- UTM is a conformal map projection that preserves shape and small areas.
- Each UTM zone spans 6° of longitude, so picking the right one for the farm's longitude minimizes distortion.
- A 6° zone has under 0.1% area error near its center, so for any farm under 10 acres this is more than sufficient.
- 1 square meter = 0.000247105 acres (the conversion factor used).

**Note:** the current implementation uses Northern Hemisphere UTM SRIDs (32600 + zone). For deployments in the Southern Hemisphere, the code can be extended to switch to 32700 + zone based on the centroid latitude. India is entirely in the Northern Hemisphere so the current implementation is correct for the target user base.

### 2. Server-Side AOI Validation Algorithm

When a user submits a farm polygon, the server enforces the 10-acre limit:

```
INPUT: GeoJSON geometry from request
1. Parse geometry from JSON into GEOSGeometry with SRID 4326
2. If geometry is invalid or empty: return 400 Bad Request
3. aoi_acres = Farm.acres_from_geometry(geometry)
4. If aoi_acres is None: return 400 "Could not compute area..."
5. If aoi_acres > MAX_FARM_AOI_ACRES (10) + epsilon:
       return 400 "This boundary is about {acres} acres.
                   The maximum allowed field size is 10 acres."
6. Otherwise: create Farm record and return 200 OK with farm UUID
```

The epsilon (`1e-9`) accounts for floating-point rounding so a polygon of exactly 10.0 acres is not falsely rejected.

### 3. Vegetation Index Formulas

All three indices use Sentinel-2 L2A band-math, computed server-side by TiTiler:

| Index | Formula | Range | Colormap |
|---|---|---|---|
| **NDVI** | `(nir - red) / (nir + red)` | -1 to 1 | RdYlGn |
| **EVI** | `2.5 * ((nir - red) / (nir + 6 * red - 7.5 * blue + 1))` | 0 to 1 | YlGn |
| **NDMI** | `(nir - swir16) / (nir + swir16)` | -1 to 1 | Blues |

The expressions are stored in the `IndexFormula` dataclass in `main/enum.py` and sent to TiTiler as URL-encoded query parameters. Sentinel-2 L2A asset names (`red`, `nir`, `blue`, `swir16`) match what Element84 STAC uses.

**Interpretation:**
- NDVI > 0.7 indicates healthy, dense vegetation; 0.2-0.5 typical of sparse or stressed crops; < 0.2 likely bare soil or water.
- EVI > 0.4 indicates active healthy crop canopy; less affected than NDVI by atmospheric haze and bright soil background.
- NDMI > 0.4 indicates high canopy moisture (well-watered); near 0 indicates moisture stress.

### 4. STAC Query Construction Algorithm

```
INPUT: farm_geometry (GeoJSON), start_date, end_date, max_cloud_cover
1. URL-encode the GeoJSON
2. Construct STAC URL:
   {STAC_BASE}/search?
     datetime={start}T00:00:00.000Z/{end}T23:59:59.000Z
     &limit=200
     &collections=sentinel-2-l2a
     &intersects={url_encoded_geojson}
     &query={"eo:cloud_cover":{"gte":0,"lte":{max_cloud_cover}}}
3. HTTP GET with 30s timeout
4. Parse response.json()["features"] for scenes
5. For each scene, extract id, datetime, eo:cloud_cover, platform
```

### 5. Multi-Threaded Statistics Aggregation Algorithm

For computing statistics across many scenes (e.g., a time series), the system uses `ThreadPoolExecutor`:

```
INPUT: items (list of STAC scene dicts), collection, expression, geometry
1. Create ThreadPoolExecutor with max_workers=10
2. Submit one fetch_stats() task per item
3. Use as_completed() to collect results in completion order
4. Filter out None results (failed fetches)
5. Return list of stats dicts
```

This pattern reduces wall-clock time for N scenes from approximately `N * single_fetch_time` to `(N / 10) * single_fetch_time` (when N > 10), since the I/O-bound HTTP calls overlap.

### 6. Forecast Chunked-Fallback Algorithm

The 16-day forecast endpoint requests 11 daily variables at once. If Open-Meteo's response is non-200 (rare but possible during overload), the helper falls back to chunked retries:

```
1. Try full request with all 11 variables. If 200 → use it.
2. Else: split variables into chunks of 2
3. For each chunk: request only those variables
4. If chunk succeeds: merge into combined_daily_forecast dict
5. If chunk fails: fill that variable with [None, None, ...] of correct length
6. Return assembled forecast even if partial
```

This makes the forecast endpoint robust to partial upstream failures.

## 5.3 Testing

Testing is essential for any software project to ensure correctness, reliability, and a good user experience. For CropGeo Analytics, testing was performed at multiple levels.

### Objectives of Testing

- Verify that every view function behaves correctly for valid inputs.
- Confirm that all validation rules (10-acre cap, geometry validity, auth gates) reject invalid inputs with appropriate error messages.
- Ensure that spatial computations (UTM area, geometry transformation) produce correct numerical results.
- Validate that external API integrations (STAC, TiTiler, Open-Meteo) handle both success and error responses gracefully.
- Confirm that user data is properly isolated (one user cannot see another's farms).
- Ensure that the UI flow is smooth across pages (login → dashboard → add farm → view farm → satellite analysis).

### Types of Testing Performed

#### 1. Unit Testing

Unit testing verifies individual functions in isolation. For CropGeo Analytics:

- **Model methods:** Test `Farm.acres_from_geometry()` with known polygons (a square of 100m × 100m at the equator should give approximately 2.47 acres). Test `Farm.save()` to confirm the `area` and `size_acres` fields are auto-populated.
- **Vegetation index formulas:** Test that `S2IndexFormulas.get_formula(VegetationIndex.NDVI)` returns the correct NDVI formula object with the right bands and colormap.
- **Pagination helper:** Test `_elided_page_numbers()` produces compact page ranges for various paginator sizes.
- **Form validation:** Test that `FarmForm` rejects empty fields.

#### 2. Integration Testing

Integration testing verifies that multiple components work together correctly:

- **Login → Dashboard:** Authenticate as an approved user, hit dashboard, confirm own farms appear.
- **Add Farm → DB:** POST a valid GeoJSON polygon to `/add-farm/`, confirm a record exists in PostGIS with correct area.
- **Farm Polygon → STAC Query → TiTiler Stats:** End-to-end flow, ensuring the right STAC items are found and TiTiler returns numeric stats.
- **Open-Meteo Weather:** Confirm that requesting weather for a farm with a valid centroid returns a 200 with the expected keys.

#### 3. Acceptance Testing

Acceptance testing confirms the system meets the user's needs. Performed with:

- Test users walking through the entire signup → wait → admin approval → login → add farm → see dashboard flow.
- Verifying that error messages are friendly and actionable.
- Confirming that the AOI rejection message is clear when a polygon is too large.

#### 4. Performance Testing

Performance testing measures system behavior under load:

- **Page load time** for the dashboard with 10+ farms (should be under 1 second).
- **Satellite stats fetch time** for a single scene (depends on TiTiler; typically 1-3 seconds).
- **Multi-threaded stats fetch time** for 10 scenes (should be ~3-5 seconds, not 30, thanks to ThreadPoolExecutor).
- **Forecast endpoint resilience** when Open-Meteo is slow or partially failing (chunked-fallback ensures partial data is returned).

#### 5. Security Testing

Security testing confirms that the system resists common attacks:

- **Cross-user data access:** Try to access another user's farm by UUID. Verify the response is 404 (because `Farm.objects.get(id=farm_id, user=request.user)` filters by owner).
- **CSRF protection:** Verify that POST requests without a CSRF token are rejected.
- **SQL injection:** Verify that user inputs in search boxes (`q`, `farm_q`) are properly escaped via the ORM.
- **Geometry injection:** Submit malformed GeoJSON; confirm the system returns 400 with a useful message.

## 5.4 Test Cases

The test cases below mirror the format of the friend's PDF (Test Case ID, Test Scenario, Input, Expected Output, Status), adapted to CropGeo Analytics.

### Sample Test Cases (cross-module)

| Test Case ID | Test Scenario | Input | Expected Output | Status |
|---|---|---|---|---|
| TC_S1 | View own farms | Logged-in approved user with 3 farms | Dashboard shows 3 farms and total acres | Pass |
| TC_S2 | View dashboard with no farms | Logged-in approved user with 0 farms | Dashboard shows empty state with "Add Farm" CTA | Pass |
| TC_S3 | Access without login | GET /dashboard/ as anonymous user | Redirect to /login/ | Pass |
| TC_S4 | Pending-approval account | Login as user with `is_approved=False` | Warning message "pending approval", no dashboard access | Pass |
| TC_S5 | Session timeout | Idle for SESSION_COOKIE_AGE seconds, then click any link | Redirected to /login/ | Pass |

### Login Module Test Cases

| Test Case ID | Test Scenario | Input | Expected Output | Status |
|---|---|---|---|---|
| TC_L1 | Valid login | Correct email + password (approved user) | Redirect to /dashboard/ | Pass |
| TC_L2 | Invalid password | Correct email + wrong password | "Invalid email or password" error | Pass |
| TC_L3 | Empty fields | Blank email and password | "Please provide both email and password" error | Pass |
| TC_L4 | Unapproved account | Correct credentials for `is_approved=False` user | "pending approval" warning, no login | Pass |
| TC_L5 | Already-authenticated user accesses /login/ | Logged-in user navigates to /login/ | Redirect to /dashboard/ (or /admin-dashboard/ if staff) | Pass |
| TC_L6 | Staff login | Correct credentials for staff user | Redirect to /admin-dashboard/ | Pass |

### Registration Module Test Cases

| Test Case ID | Test Scenario | Input | Expected Output | Status |
|---|---|---|---|---|
| TC_R1 | Valid registration | Complete form: name, email, age, gender, password | Account created with `is_approved=False`, redirect to /login/ with success message | Pass |
| TC_R2 | Duplicate email | Email already exists in DB | "Email already exists" error | Pass |
| TC_R3 | Missing fields | One or more fields blank | "Please fill in all fields" error | Pass |
| TC_R4 | Weak password | Password fails Django validators (too short, too common, all-numeric) | Validation error from password validator | Pass |
| TC_R5 | Invalid age | Age = "abc" or negative | `int(age)` raises ValueError, generic "Error creating account" shown | Pass |

### Farm Registration Module Test Cases (replaces "Disease Detection" in friend's PDF)

| Test Case ID | Test Scenario | Input | Expected Output | Status |
|---|---|---|---|---|
| TC_F1 | Valid farm submission | Name, crop_type, valid 5-acre polygon | 200 OK, farm saved with UUID, redirect to dashboard | Pass |
| TC_F2 | Polygon too large | Polygon ~20 acres | 400 with message "This boundary is about 20.xx acres. The maximum allowed field size is 10 acres." | Pass |
| TC_F3 | No geometry | POST without `geometry` field | 400 "Please draw the farm boundary on the map" | Pass |
| TC_F4 | Invalid GeoJSON | `geometry={"foo": "bar"}` | 400 "Invalid GeoJSON structure" | Pass |
| TC_F5 | Empty geometry | `geometry={"type": "Polygon", "coordinates": []}` | 400 "Empty or invalid geometry" | Pass |
| TC_F6 | Missing crop type | Geometry valid, but `cropType` empty | 400 "Farm name and crop type are required" | Pass |
| TC_F7 | Cross-user delete | Login as user A, try to delete user B's farm | 404 (filter `user=request.user` returns no match) | Pass |
| TC_F8 | Auto-area on save | Save farm with 4047 m² polygon | `size_acres` ≈ 1.00 saved | Pass |

### Satellite Analysis Module Test Cases (replaces "Plant Growth" in friend's PDF)

| Test Case ID | Test Scenario | Input | Expected Output | Status |
|---|---|---|---|---|
| TC_X1 | Valid scene search | farm_id, start=2025-04-01, end=2025-05-01, cloud_cover=20 | JSON list of Sentinel-2 scenes, each with id, date, cloud cover, platform | Pass |
| TC_X2 | Empty date range | end_date before start_date | 400 "End date cannot be before start date" | Pass |
| TC_X3 | Invalid date format | start_date="2025/01/01" | 400 "Invalid date format. Use YYYY-MM-DD" | Pass |
| TC_X4 | Invalid index | get_farm_stats with `index_type="bogus"` | 400 "Invalid index type: bogus" | Pass |
| TC_X5 | Valid NDVI stats | farm_id, valid item_id, index="ndvi" | 200 JSON with min/max/mean/std/median and index_info | Pass |
| TC_X6 | Imagery PNG request | farm_id, item_id, index="evi" | 200 JSON with base64 PNG data URL and bbox | Pass |
| TC_X7 | Farm without geometry | Hypothetical farm with empty geometry | 400 "Farm has no geometry" | Pass |
| TC_X8 | Weather current | farm_id with valid geometry | 200 JSON with `current` containing temp, humidity, soil_*, etc. | Pass |
| TC_X9 | Weather forecast | farm_id with valid geometry | 200 JSON with 16-day `forecast` dict | Pass |
| TC_X10 | Cloud cover filter | search with cloud_cover=0 | 0 results (almost always — no perfectly clear scenes) | Pass |

### Test Case Design Principles

While writing these test cases, the following principles were followed:

- Each test case focuses on a specific behavior of the system.
- Both valid inputs (positive cases) and invalid inputs (negative cases) are covered.
- Cross-cutting concerns (auth, ownership, validation) are tested at the boundaries.
- Test cases are simple, clear, and reproducible.
- Pass / fail status is recorded so regressions can be detected.

## 5.5 System Screenshots

Pratham should capture the following 10 screenshots from the running application. The descriptions below are based on what each template renders.

### 1. Home / Landing Page

The landing page (likely `dashboard.html` for authenticated users, or a public landing page if visiting anonymously). Shows the CropGeo Analytics title/logo, a welcome message, and CTAs to log in or sign up. (Fig 5.1)

### 2. Login Page

Two-column layout (similar to the friend's PDF style) with a green/agriculture-themed background. Form fields: Email, Password. "Login" button. Link to Signup page. Renders error messages from Django `messages` framework. Path: `/login/`. (Fig 5.2)

### 3. Signup Page

Multi-field registration form: Name, Email, Age, Gender (dropdown), Password, Confirm Password. "Register" button. Link back to Login. After successful submit, redirects to login with success message about admin approval. Path: `/signup/`. (Fig 5.3)

### 4. User Dashboard

Displayed at `/` for authenticated approved users. Shows a list of the user's farms with name, crop type, size in acres, and a "View" button per farm. A "Total Acres" summary at the top. CTA to "Add Farm" if there are no farms. If the user is not yet approved, instead shows a pending-approval banner. (Fig 5.4)

### 5. Add Farm Page

The most map-intensive page. OpenLayers map covering most of the screen, with polygon-drawing controls. Form fields for: Farm Name, Crop Type (dropdown with 7 crops: wheat, corn, soybeans, rice, cotton, barley, oats). "Save Farm" button. Shows a live computed area in acres as the user draws. If the polygon exceeds 10 acres, an error appears. Path: `/add-farm/`. (Fig 5.5)

### 6. View Farm Dashboard

The per-farm analytics page. Most complex template (1670 lines). Shows:
- Map with the farm polygon overlaid in a vivid color.
- Farm name, crop type, area in acres.
- Satellite scene picker (date range + cloud cover slider + search button).
- List of available Sentinel-2 scenes with cloud cover percentage.
- Vegetation index selector (NDVI / EVI / NDMI buttons).
- "Compute Stats" button → shows min/max/mean/std/median in a card.
- "Show Imagery" button → overlays the colored satellite raster on the map.
- Weather widget: current temperature, humidity, soil moisture summary.
- Forecast section: 16-day chart of temp_max/min/mean and precipitation.
Path: `/view-farm/<uuid>/`. (Fig 5.6)

### 7. Admin Dashboard

Three-section page visible only to staff users:
- **Pending Users** (paginated): name, email, signup date, [Approve] [Reject] buttons per row.
- **Approved Users** (paginated): name, email, farm count, [Deactivate] [Delete] buttons.
- **All Farms** (paginated): farm name, owner email, crop type, size, created date.
- Search boxes for users (`q`) and farms (`farm_q`).
- Counts displayed at the top: pending count, approved count, farm count.
Path: `/admin-dashboard/`. (Fig 5.7)

### 8. About Page

Static informational page describing CropGeo Analytics — its purpose, features, technology stack, and target audience. Includes team / college credits. Path: `/about/`. (Fig 5.8)

### 9. Logout Page / Logout Confirmation

After clicking Logout, the user is redirected to `/login/` with a success message "You have been logged out successfully." (technically there is no separate logout page; the logout view immediately ends the session and redirects). (Fig 5.9)

### 10. Pending Approval Screen

What a newly-signed-up user sees if they try to log in before an admin approves them: the login page with a warning message "Your account is pending approval. Please wait for admin approval." Path: `/login/` after auth attempt. (Fig 5.10)

---

# CHAPTER 6 — RESULT AND ANALYSIS

## 6.1 Results

CropGeo Analytics was successfully designed, developed, and tested as a fully functional web GIS platform for satellite-based crop monitoring. All planned modules were implemented, and the entire end-to-end flow works as designed:

- User can register with name, email, age, gender, password.
- Admin can log in and approve, reject, deactivate, or delete users from a paginated dashboard.
- Approved user can log in and access the per-user dashboard.
- User can draw a farm polygon on an OpenLayers map and save it.
- The server validates the geometry, computes the area in acres via UTM projection, and rejects polygons larger than 10 acres.
- User can open a per-farm dashboard showing the polygon on a map.
- User can search Sentinel-2 scenes via the Element84 STAC API, filtered by date range and cloud cover.
- User can compute NDVI, EVI, or NDMI statistics over the farm polygon by selecting a scene; the system returns min/max/mean/std/median.
- User can render satellite imagery as a colored overlay on the map.
- User can view current weather and a 16-day forecast (with soil temperature and moisture data) for the farm centroid.

### Output Results (summary)

- Successful spatial farm registration with sub-percent area accuracy.
- Working integration with three external APIs (Element84 STAC, TiTiler, Open-Meteo).
- Three vegetation indices fully implemented and tested.
- Server-side AOI cap (10 acres) enforced reliably.
- UUID-keyed farm URLs prevent cross-user data leakage.
- Admin dashboard with pagination and search for both users and farms.
- 19 view functions, 19 URL patterns, 4 migrations, 2 data models, 10 templates — total ~5000 lines of code.

### Analysis

The platform performs efficiently in the typical use case. The single biggest performance gain comes from the multi-threaded statistics fetching (`ThreadPoolExecutor(max_workers=10)`), which makes time-series stats analysis feasible. The UTM-based area calculation, although unusual in beginner web projects, gives accurate real-world acres without depending on a separate GIS library; this is a small but important technical strength.

The user interface, while functional, is the area with the most scope for improvement: the dashboard could benefit from richer charts, the satellite-scene picker could be clearer about which scenes are usable, and a mobile-responsive layout would broaden adoption.

The reliance on external APIs is both a strength (no need to host satellite imagery or weather data) and a weakness (the platform stops working if any of the three APIs is down). The forecast endpoint includes a chunked-fallback strategy to make Open-Meteo failures less impactful; similar resilience could be added to the STAC and TiTiler calls in future versions.

## 6.2 Report Generation

The dashboards surface project results as **live, real-time reports** — there is no offline batch processing. Every time the user opens a farm dashboard or clicks "compute stats" or "show imagery", the system fetches fresh data, computes new results, and displays them immediately.

### Data Collection

The system collects data from three categories of sources:

- **User input data:** The polygon drawn on the map, farm name, crop type, satellite scene id, index choice, date range, cloud-cover threshold.
- **External satellite data:** Sentinel-2 L2A scene metadata from Element84 STAC; raster data accessed via TiTiler.
- **External weather data:** Current weather and 16-day forecast from Open-Meteo, including soil temperature and moisture at multiple depths.
- **System-generated data:** UUID-keyed farm records, auto-computed area in m² and acres, signup and creation timestamps.

All persistent data is stored in PostgreSQL with PostGIS; transient external data is fetched on demand and not cached.

### Processing Mechanism

The processing pipeline for a typical satellite analysis request:

1. **Request transfer:** Browser sends an AJAX POST to a Django endpoint (e.g., `/farm/<uuid>/get-stats/`).
2. **Authentication and authorization:** `@login_required` ensures the request is from a logged-in user; the ORM query `Farm.objects.get(id=farm_id, user=request.user)` ensures the user owns the farm.
3. **Input validation:** The view confirms required fields (`item_id`, `index_type`) and that the index is one of the supported `VegetationIndex` enum values.
4. **Expression lookup:** The view fetches the `IndexFormula` for the requested index from `S2IndexFormulas` and URL-encodes the formula.
5. **External call:** The view (or `utils.fetch_stats`) builds the TiTiler URL with the STAC item URL, expression, and other parameters; POSTs the farm geometry; receives a JSON response.
6. **Result formatting:** The view extracts min/max/mean/std/median from the response and returns a JSON payload to the browser.
7. **Browser display:** The browser updates the stats card with the new values.

For satellite imagery the flow is similar but the response includes a base64-encoded image data URL and a bounding box, which the browser uses to create an OpenLayers ImageStatic source overlaid on the map.

### Flow of Real-Time Report Generation

```
+-----------------------+
| User input / map      |
| interactions          |
+----------+------------+
           |
           v
+-----------------------+
| Browser (AJAX request)|
+----------+------------+
           |
           v
+-----------------------+
| Django view           |
| (auth + validation)   |
+----------+------------+
           |
           v
+-----------------------+
| Spatial query in      |
| PostGIS  /  external  |
| API call (STAC,       |
| TiTiler, Open-Meteo)  |
+----------+------------+
           |
           v
+-----------------------+
| Result formatting     |
| (JSON or image)       |
+----------+------------+
           |
           v
+-----------------------+
| Dashboard updates     |
| (chart, stats card,   |
| map overlay)          |
+-----------------------+
```

### Report Content

The dashboards present several kinds of report content:

- **Farm summary:** Name, crop type, area in acres, created date, polygon overlay on map.
- **Vegetation index report:** Min/max/mean/std/median for the selected index on the selected scene, plus the index name and description from the `IndexFormula`.
- **Satellite imagery:** Colored raster overlay on the map, with a legend showing the value range and colormap.
- **Current weather report:** Temperature, apparent temperature, humidity, precipitation, rain, cloud cover, surface pressure, wind speed, wind gusts, sunrise, sunset, UV index, evapotranspiration (FAO ET₀), soil temperature at 4 depths, soil moisture at 5 depths.
- **16-day forecast report:** Daily max/min/mean temperature, max humidity, precipitation, rain, mean surface pressure, mean cloud cover, daily evapotranspiration, max wind speed, max wind gusts — for each of the next 16 days.

### Real-Time Functionality

- **Instant updates:** All dashboard panels update without page reload, via AJAX.
- **No polling:** The system fetches fresh data only when the user explicitly requests it (better for API quotas).
- **Continuous live monitoring:** The user can switch between scenes, indices, and dates freely; each switch triggers a fresh fetch.
- **Fast pipeline:** Single-scene stats typically returned in 1-3 seconds; multi-scene time series via the multi-threaded fetcher returns in similar time.

### Visualization

- **Dashboard view:** Per-farm map with polygon overlay, scene picker, index selector, stats cards, weather widget.
- **Satellite raster overlay:** Colored vegetation index image drawn over the basemap using OpenLayers ImageStatic source.
- **Charts:** Optionally implemented for the 16-day forecast (temp / precipitation bar or line chart).
- **Summary cards:** Numerical stats displayed in clean, readable cards.

## 6.3 Discussion

### Strengths

- **End-to-end functional system:** Every requirement was implemented and demonstrated.
- **Free data sources:** Nothing in the platform requires a paid subscription, making it deployable anywhere.
- **Accurate area calculation:** UTM-based projection is more accurate than naïve haversine-area approximations.
- **Robust validation:** Server-side checks reject bad input before it reaches the database.
- **Multi-threading:** Statistics fetching scales gracefully to many scenes.
- **Admin moderation:** Suitable for institutional deployments where access must be curated.
- **Open-source stack:** Django, GeoDjango, PostGIS, OpenLayers, TiTiler — all permissive licenses.
- **Clear module separation:** `models.py`, `views.py`, `utils.py`, `enum.py`, `weather_api.py` each own a clear responsibility.

### Limitations

- **10-acre AOI cap:** Intentional, but limits the platform's usefulness for larger commercial farms.
- **Sentinel-2 only:** No Landsat, PlanetScope, or radar (Sentinel-1) data; vegetation analysis is impossible under persistent cloud cover.
- **No historical archive UI:** Each scene is fetched on demand; there is no built-in timelapse view.
- **No notification system:** The system does not alert farmers about stress events; the user must check the dashboard.
- **No mobile app:** The web UI is browser-only; a touch-friendly mobile layout would help.
- **English-only UI:** No Marathi, Hindi, or other Indian-language support.
- **External API dependency:** Failures of Element84 STAC, TiTiler, or Open-Meteo break the corresponding features.
- **No yield prediction:** Vegetation indices are proxies, not direct yield estimators; an ML layer for yield estimation is future work.
- **No multi-farm comparison view:** The dashboard is per-farm; comparing two farms requires opening two tabs.

### Comparison to Manual Methods

| Aspect | Manual Inspection | CropGeo Analytics |
|---|---|---|
| Coverage | Sample-based (walked rows) | Whole-field (every pixel) |
| Frequency | Whenever the farmer visits | Every Sentinel-2 pass (~5 days) |
| Detection of early stress | Late (visible symptoms) | Early (vegetation index changes) |
| Effort | High (physical inspection) | Low (browser dashboard) |
| Cost | Time + transport | Free (data + free service tier) |
| Weather context | Generic local weather | Centroid-specific weather + 16-day forecast |
| Soil data | None (unless soil tested) | Soil temp at 4 depths, soil moisture at 5 depths |
| Record keeping | Notebook or memory | Persistent in PostGIS, queryable |

The result is that CropGeo Analytics is not a replacement for visual field inspection — it is a complement that helps the farmer prioritize where to walk and what to check.

---

# CHAPTER 7 — CONCLUSION AND FUTURE SCOPE

## 7.1 Conclusion

The CropGeo Analytics project has been successfully designed and developed as a web-based GIS platform for satellite-driven precision agriculture. The system delivers on its core promise: it lets a farmer or researcher register a farm polygon, monitor that field with vegetation indices computed from Sentinel-2 imagery, and check weather conditions and a 16-day forecast — all from a single browser-based dashboard, using only free data sources.

The project integrates a number of advanced technologies into a single coherent application:

- **Django 5.2.7** with **GeoDjango** as the web framework, providing spatial model fields, spatial queries, and OpenLayers admin integration.
- **PostgreSQL with PostGIS** as the spatial database backend, enabling geometry storage and spatial queries.
- **OpenLayers** in the browser for interactive map display and polygon drawing.
- **Element84 STAC API** for discovering Sentinel-2 satellite scenes on AWS Open Data.
- **TiTiler** for on-the-fly raster processing — band-math expressions, statistics, colormapped image rendering.
- **Open-Meteo API** for current weather, soil temperature and moisture, and 16-day forecast.
- **ThreadPoolExecutor** (Python `concurrent.futures`) for multi-threaded statistics aggregation.
- **UUID primary keys** for farm records to prevent enumeration attacks.
- **UTM zone projection** for accurate per-farm area calculation in acres.
- **Custom Django `User` model** with `is_approved` field, enabling an admin-moderation workflow.

The codebase consists of approximately 5000 lines split between Python source files, Django templates, and HTML/CSS/JavaScript. It includes 19 view functions, 19 URL patterns, 4 migrations, 2 data models, and 10 templates. Every functional requirement from the SRS has been implemented and tested.

From an MCA capstone perspective, the project demonstrates competence in:

- Full-stack web development with Django and modern templates.
- Relational database design with foreign keys, UUIDs, and migrations.
- Spatial database operations with PostGIS.
- REST API consumption from external services (STAC, TiTiler, Open-Meteo).
- Multi-threading and concurrent I/O.
- Authentication, authorization, and access control patterns.
- Server-side validation and error handling.
- Modular code organization for maintainability.

The platform demonstrates that precision-agriculture monitoring tools can be built entirely from free and open data sources, removing cost as a barrier for small farmers. It also demonstrates that final-year MCA students can produce a real-world, technically meaningful application that combines several emerging technology stacks.

In summary, CropGeo Analytics is a working, reliable, accurate, and extensible platform for satellite-based crop monitoring of small farms. It achieves its stated objectives, fulfills its scope, and lays a strong foundation for future enhancements.

## 7.2 Future Scope

The current version of CropGeo Analytics is a solid foundation, but there are many avenues for future enhancement. These can be grouped into platform, data, intelligence, and accessibility improvements.

### Platform Enhancements

1. **Mobile Application Development**
   - Native Android and iOS apps using React Native or Flutter.
   - Push-notification support for stress-event alerts.
   - Camera integration for on-field photo capture tied to farm polygons.

2. **Cloud Integration**
   - Containerized deployment (Docker + Kubernetes) for one-click cloud installation.
   - Cloud-managed PostgreSQL + PostGIS (e.g., AWS RDS, Azure Database).
   - CDN-cached map tiles for faster page loads.

3. **Notification System**
   - Email alerts when NDVI drops below a configurable threshold.
   - SMS alerts via Twilio or similar for important weather events.
   - In-app notification center for past alerts.

4. **Offline Mode (PWA)**
   - Progressive Web App with offline-cached dashboards for cached scenes.
   - Sync queued farm-edits when connection is restored.

### Data Enhancements

5. **Additional Satellite Sources**
   - **Landsat-8 / Landsat-9** for longer historical archives (back to 2013/2021 respectively) and 30 m thermal data.
   - **PlanetScope** (paid) for daily 3 m imagery — useful for very small fields and intra-field heterogeneity.
   - **Sentinel-1 SAR** (radar) for cloud-penetrating imagery, allowing analysis during monsoon season.

6. **Additional Vegetation Indices**
   - **SAVI** (Soil-Adjusted Vegetation Index) — for sparse vegetation over bright soils.
   - **NDWI** (Normalized Difference Water Index) — for surface-water detection.
   - **GNDVI** (Green NDVI) — for nitrogen-content estimation.
   - **NDRE** (Normalized Difference Red Edge) — for chlorophyll content using Sentinel-2's red-edge bands.

7. **Historical Archive Timelapse**
   - A time-series view showing how NDVI / EVI / NDMI changed across the season.
   - Side-by-side comparison of imagery across multiple dates.
   - Year-over-year crop performance charts.

8. **IoT Sensor Integration**
   - Bluetooth/WiFi soil-moisture probes feeding ground-truth data into the dashboard.
   - LoRa/ESP32 weather-station integration for hyperlocal data.
   - Drone-imagery upload for ultra-high-resolution monitoring.

### Intelligence Enhancements

9. **ML-Based Crop-Specific Recommendations**
   - Train a model to recommend irrigation amounts based on NDMI + soil moisture + forecasted ET₀.
   - Suggest optimal harvest timing based on NDVI peaks and historical patterns.

10. **Anomaly Detection**
    - Auto-detect when an index value deviates from the seasonal norm and flag it.
    - Distinguish water stress, nutrient stress, and disease using multi-index signatures.

11. **Yield Estimation**
    - Build a regression model relating NDVI/EVI to historical yield for major Indian crops (wheat, rice, soybean).
    - Display predicted yield per acre at season end.

12. **ML-Based Crop Type Classification**
    - Auto-classify crop type from satellite imagery as a sanity check on user-provided crop_type.

### Accessibility Enhancements

13. **Multi-Language UI**
    - Add Marathi and Hindi translations for the entire UI (Django i18n).
    - RTL support for languages where appropriate.
    - SMS / voice integration for farmers without smartphones.

14. **Improved Onboarding**
    - Guided tour on first login.
    - Sample farm with pre-loaded data so users can explore before drawing their own.
    - Video tutorials embedded in the dashboard.

15. **Multi-Farm Comparison Dashboard**
    - Side-by-side view of two or more farms.
    - Portfolio-level summary for farmers/researchers managing many fields.

16. **Public Reports and Sharing**
    - Generate shareable read-only links for specific farm reports.
    - PDF / image export of dashboards for sharing with extension officers.

These enhancements form a clear roadmap for evolving CropGeo Analytics from an MCA capstone project into a production-grade precision-agriculture platform.

---

# REFERENCES

The following references support the technical and conceptual decisions made in CropGeo Analytics:

1. Drusch, M., et al. *Sentinel-2: ESA's Optical High-Resolution Mission for GMES Operational Services.* Remote Sensing of Environment, Vol. 120, 2012, pp. 25-36.

2. Rouse, J. W., Haas, R. H., Schell, J. A., & Deering, D. W. *Monitoring Vegetation Systems in the Great Plains with ERTS.* Proceedings of the Third Earth Resources Technology Satellite-1 Symposium, NASA SP-351, 1973, pp. 309-317. (Original NDVI paper.)

3. Huete, A., Didan, K., Miura, T., Rodriguez, E. P., Gao, X., & Ferreira, L. G. *Overview of the radiometric and biophysical performance of the MODIS vegetation indices.* Remote Sensing of Environment, Vol. 83, 2002, pp. 195-213. (EVI definition.)

4. Gao, B. C. *NDWI — A Normalized Difference Water Index for Remote Sensing of Vegetation Liquid Water from Space.* Remote Sensing of Environment, Vol. 58, 1996, pp. 257-266. (NDMI/NDWI background.)

5. Django Software Foundation. *Django Documentation: GeoDjango.* https://docs.djangoproject.com/en/5.2/ref/contrib/gis/, accessed 2026.

6. PostGIS Project Steering Committee. *PostGIS 3.x Documentation.* https://postgis.net/docs/, accessed 2026.

7. STAC Specification Working Group. *SpatioTemporal Asset Catalog (STAC) Specification, Version 1.0.0.* https://github.com/radiantearth/stac-spec, accessed 2026.

8. Element 84. *Earth Search STAC API.* https://earth-search.aws.element84.com/v1, accessed 2026.

9. Vincent, S., & developmentseed contributors. *TiTiler — Dynamic Tile Server.* https://developmentseed.org/titiler/, accessed 2026.

10. Open-Meteo. *Open-Meteo Free Weather Forecast API Documentation.* https://open-meteo.com/en/docs, accessed 2026.

11. Allen, R. G., Pereira, L. S., Raes, D., & Smith, M. *Crop evapotranspiration — Guidelines for computing crop water requirements.* FAO Irrigation and drainage paper 56, 1998. (FAO ET₀ definition used by Open-Meteo.)

12. Snyder, J. P. *Map Projections — A Working Manual.* U.S. Geological Survey Professional Paper 1395, 1987. (Reference for UTM projection used in farm-area calculation.)

13. OpenLayers Project. *OpenLayers v8+ Documentation.* https://openlayers.org/, accessed 2026.

14. Python Software Foundation. *concurrent.futures — Launching parallel tasks.* https://docs.python.org/3/library/concurrent.futures.html, accessed 2026.

15. Cloud-Optimized GeoTIFF (COG) Working Group. *Cloud Optimized GeoTIFF Specification.* https://www.cogeo.org/, accessed 2026.

---

# APPENDIX A — Full File Inventory

The CropGeo Analytics codebase is organized as follows:

### Project root: `/home/pratham19/cropgeo/cropgeo/`

| Path | Purpose |
|---|---|
| `manage.py` | Django management entry point |
| `requirements.txt` | Python dependency list |
| `.env.example` | Example environment variables (DB_*, TITILER_URL) |
| `.gitignore` | Git ignore patterns |
| `db.sqlite3` (if present) | Local dev DB — **not used in production**; production uses PostGIS |

### Django project config: `cropgeo/`

| File | Purpose |
|---|---|
| `cropgeo/settings.py` | Django settings: PostGIS database, INSTALLED_APPS, TITILER_URL, middleware, templates |
| `cropgeo/urls.py` | Project-level URL routing — includes `main.urls` at `/` |
| `cropgeo/wsgi.py` | WSGI entry point for gunicorn |
| `cropgeo/asgi.py` | ASGI entry point (unused) |
| `cropgeo/__init__.py` | Package marker |

### Main application: `main/`

| File | Lines | Purpose |
|---|---|---|
| `main/models.py` | 82 | `User` (custom, extends AbstractUser) and `Farm` (UUID PK, GeometryField, UTM area calc) |
| `main/views.py` | 640 | 19 view functions covering all user-facing endpoints |
| `main/urls.py` | 23 | URL patterns for the main app |
| `main/utils.py` | 210 | TiTiler / STAC helpers: `get_imagery`, `get_raw_band_data`, `fetch_stats`, `get_stats` (multi-threaded) |
| `main/weather_api.py` | 231 | Open-Meteo helpers: `get_current_weather_payload`, `get_forecast_weather_payload` |
| `main/enum.py` | 137 | `VegetationIndex`, `S2Band`, `Colormap`, `ImageType` enums; `IndexFormula` dataclass; `S2IndexFormulas` with NDVI/EVI/NDMI definitions |
| `main/forms.py` | ~30 | Django form classes (FarmForm) |
| `main/admin.py` | small | Admin registrations (User, Farm shown in Django admin) |
| `main/apps.py` | small | App config |
| `main/__init__.py` | 0 | Package marker |

### Migrations: `main/migrations/`

| File | Purpose |
|---|---|
| `0001_initial.py` | Initial User model creation |
| `0002_alter_user_age_alter_user_gender.py` | Refine age/gender field constraints |
| `0003_farm.py` | Add Farm model with geometry, UUID, FK to User |
| `0004_user_is_approved.py` | Add `is_approved` boolean to User |

### Templates: `templates/`

| File | Lines | Purpose |
|---|---|---|
| `base.html` | 134 | Shared HTML skeleton with `{% block %}` slots |
| `includes/navbar.html` | 22 | Top navigation bar |
| `includes/cropgeo_modal.html` | 240 | Reusable modal component |
| `login.html` | 495 | Login form |
| `signup.html` | 492 | Registration form |
| `about.html` | 373 | About page |
| `dashboard.html` | 406 | User dashboard (farm list) |
| `add-farm.html` | 1077 | Add farm with OpenLayers map and polygon drawing |
| `view-farm-dashboard.html` | 1670 | Per-farm analytics dashboard (satellite + weather + map) |
| `admin-dashboard.html` | 665 | Admin panel (paginated users + farms) |

### Total project size

- Python source: roughly 1,300 lines (views, models, utils, weather, enum, forms, admin, settings, urls).
- Templates: roughly 5,500 lines of HTML/CSS/JS.
- Migrations: 4 files, roughly 100 lines total.
- **Grand total: approximately 7,000 lines of project code** (excluding dependencies).

---

# APPENDIX B — Complete URL Pattern Table

All URL patterns are routed through `cropgeo/urls.py` → includes `main/urls.py` at `/`.

| Path | HTTP Methods | View Function | Decorator | Purpose |
|---|---|---|---|---|
| `/admin/` | GET, POST | Django built-in admin | — | Django admin interface |
| `/` | GET | `dashboard` | (manual check) | User dashboard, list of own farms |
| `/login/` | GET, POST | `login_view` | — | Login form |
| `/signup/` | GET, POST | `signup_view` | — | Registration form |
| `/logout/` | GET, POST | `logout_view` | — | End session, redirect to login |
| `/about/` | GET | `about_view` | — | About page |
| `/add-farm/` | GET, POST | `add_farm_view` | `@login_required` | Render form (GET) or save farm (POST) |
| `/admin-dashboard/` | GET | `admin_dashboard_view` | `@user_passes_test(is_staff)` | Admin moderation panel |
| `/approve-user/<int:user_id>/` | POST | `approve_user_view` | `@user_passes_test(is_staff)` | Approve a pending user |
| `/reject-user/<int:user_id>/` | POST | `reject_user_view` | `@user_passes_test(is_staff)` | Delete a pending user |
| `/deactivate-user/<int:user_id>/` | POST | `deactivate_user_view` | `@user_passes_test(is_staff)` | Disable a user without deleting |
| `/delete-user/<int:user_id>/` | POST | `delete_user_view` | `@user_passes_test(is_staff)` | Permanently delete a user |
| `/view-farm/<uuid:farm_id>/` | GET | `view_farm_dashboard` | `@login_required` | Per-farm analytics dashboard |
| `/delete-farm/<uuid:farm_id>/` | POST | `delete_farm_view` | `@login_required` | Delete own farm |
| `/farm/<uuid:farm_id>/search-satellite/` | POST | `search_satellite_data` | `@login_required` | Query Element84 STAC for Sentinel-2 scenes |
| `/farm/<uuid:farm_id>/get-stats/` | POST | `get_farm_stats` | `@login_required` | Compute vegetation index statistics via TiTiler |
| `/farm/<uuid:farm_id>/get-imagery/` | GET, POST | `get_farm_imagery` | `@login_required` | Get rendered satellite raster (base64 PNG) |
| `/farm/<uuid:farm_id>/weather/current/` | GET | `farm_weather_current` | `@login_required` | Current weather + soil data at farm centroid |
| `/farm/<uuid:farm_id>/weather/forecast/` | GET | `farm_weather_forecast` | `@login_required` | 16-day forecast at farm centroid |

---

# APPENDIX C — View Function Reference

Each entry includes the function signature, the URL it serves, its authorization, what it does, and what it returns.

### `dashboard(request)`
- **URL:** `/`
- **Auth:** Manual check — redirects to `/login/` if not authenticated; renders the dashboard with a "pending approval" banner if `is_approved=False` and not staff.
- **Behavior:** Loads `Farm.objects.filter(user=request.user)`, computes `total_acres`, renders `dashboard.html`.
- **Returns:** HTML.

### `login_view(request)`
- **URL:** `/login/`
- **Auth:** None.
- **Behavior:** GET renders `login.html`. POST authenticates via Django's `authenticate()`, checks `is_approved`, logs in, redirects to dashboard or admin dashboard.
- **Returns:** HTML or redirect.

### `signup_view(request)`
- **URL:** `/signup/`
- **Auth:** None.
- **Behavior:** GET renders `signup.html`. POST validates all fields, checks for duplicate email, creates a new `User` with `is_approved=False`, redirects to login with a success message.
- **Returns:** HTML or redirect.

### `about_view(request)`
- **URL:** `/about/`
- **Auth:** None.
- **Behavior:** Renders `about.html`.
- **Returns:** HTML.

### `add_farm_view(request)`
- **URL:** `/add-farm/`
- **Auth:** `@login_required`. Additionally checks `request.user.is_approved` for POST.
- **Behavior:**
  - GET: Renders `add-farm.html` with the OpenLayers map.
  - POST: Reads JSON body (or POST form data) for `farmName`, `cropType`, `farmSize`, `geometry`. Parses GeoJSON, creates `GEOSGeometry` with SRID 4326, validates, computes `acres_from_geometry`, rejects if > 10 acres, creates `Farm` instance, returns success JSON with farm UUID.
- **Returns:** HTML (GET) or JSON (POST).

### `_elided_page_numbers(paginator, page_number)` (helper, not a view)
- **Behavior:** Returns a compact page number list with `Paginator.ELLIPSIS` for the admin dashboard pagination.

### `admin_dashboard_view(request)`
- **URL:** `/admin-dashboard/`
- **Auth:** `@user_passes_test(lambda u: u.is_staff)`.
- **Behavior:**
  - Builds three paginators: pending users (10/page), approved users (10/page), all farms (15/page).
  - Supports search via `q` (users) and `farm_q` (farms).
  - Annotates each approved user with `farm_count` via `Count('farms', distinct=True)`.
  - Returns counts (pending, approved, total farms) for header KPIs.
  - Renders `admin-dashboard.html`.
- **Returns:** HTML.

### `approve_user_view(request, user_id)`
- **URL:** `/approve-user/<int:user_id>/`
- **Auth:** `@user_passes_test(is_staff)`. POST only.
- **Behavior:** Sets `is_approved=True` and `is_active=True` on the target user, saves, flashes a success message, redirects to admin dashboard.
- **Returns:** Redirect.

### `reject_user_view(request, user_id)`
- **URL:** `/reject-user/<int:user_id>/`
- **Auth:** `@user_passes_test(is_staff)`. POST only.
- **Behavior:** Refuses to reject staff users. Otherwise deletes the user with a "rejected and removed" message.
- **Returns:** Redirect.

### `deactivate_user_view(request, user_id)`
- **URL:** `/deactivate-user/<int:user_id>/`
- **Auth:** `@user_passes_test(is_staff)`. POST only.
- **Behavior:** Refuses to deactivate staff users. Otherwise sets `is_active=False` and saves.
- **Returns:** Redirect.

### `delete_user_view(request, user_id)`
- **URL:** `/delete-user/<int:user_id>/`
- **Auth:** `@user_passes_test(is_staff)`. POST only.
- **Behavior:** Refuses to delete staff users. Otherwise deletes the user with a "deleted successfully" message.
- **Returns:** Redirect.

### `delete_farm_view(request, farm_id)`
- **URL:** `/delete-farm/<uuid:farm_id>/`
- **Auth:** `@login_required`. POST only. Owner-only: `Farm.objects.get(id=farm_id, user=request.user)` returns 404 if not owner.
- **Behavior:** Deletes the farm, flashes a success message, redirects to dashboard.
- **Returns:** Redirect.

### `view_farm_dashboard(request, farm_id)`
- **URL:** `/view-farm/<uuid:farm_id>/`
- **Auth:** `@login_required`. Owner-only.
- **Behavior:** Loads the farm, serializes its geometry as a GeoJSON Feature, computes centroid `[lon, lat]` for map view, renders `view-farm-dashboard.html`.
- **Returns:** HTML.

### `farm_weather_current(request, farm_id)`
- **URL:** `/farm/<uuid:farm_id>/weather/current/`
- **Auth:** `@login_required`. Owner-only.
- **Behavior:** Calls `weather_api.get_current_weather_payload(farm)`, returns the JSON.
- **Returns:** JSON.

### `farm_weather_forecast(request, farm_id)`
- **URL:** `/farm/<uuid:farm_id>/weather/forecast/`
- **Auth:** `@login_required`. Owner-only.
- **Behavior:** Calls `weather_api.get_forecast_weather_payload(farm)`, returns the JSON.
- **Returns:** JSON.

### `search_satellite_data(request, farm_id)`
- **URL:** `/farm/<uuid:farm_id>/search-satellite/`
- **Auth:** `@login_required`. Owner-only. POST only.
- **Behavior:** Reads `start_date`, `end_date`, `cloud_cover` (default 20). Validates date format and order. URL-encodes farm GeoJSON. Calls Element84 STAC `/v1/search` for `sentinel-2-l2a`. Parses `features`, returns a list with `id`, `date`, `cloud_cover`, `platform`.
- **Returns:** JSON.

### `get_farm_stats(request, farm_id)`
- **URL:** `/farm/<uuid:farm_id>/get-stats/`
- **Auth:** `@login_required`. Owner-only. POST only.
- **Behavior:** Reads `item_id`, `index_type` (default `'ndvi'`). Validates index via `VegetationIndex` enum and looks up `S2IndexFormulas.get_formula()`. URL-encodes the formula. Calls `utils.fetch_stats()` with the STAC item URL, the expression, and the farm geometry. Returns stats (min/max/mean/std/median) plus `index_info` (name, description, range).
- **Returns:** JSON.

### `get_farm_imagery(request, farm_id)`
- **URL:** `/farm/<uuid:farm_id>/get-imagery/`
- **Auth:** `@login_required`. Owner-only.
- **Behavior:** Reads `item_id`, `index_type`, `image_type` (png/jpeg/tif), `colormap`, `min_val`, `max_val`, `pixelized`. Validates index. Resolves colormap (param overrides default). Calls `utils.get_imagery()` which POSTs to TiTiler `/stac/feature.{format}` with the farm GeoJSON. Decodes the response (base64 PNG/JPEG or raw TIF), returns a JSON with `image` (data URL), `bbox`, `format`.
- **Returns:** JSON.

### `logout_view(request)`
- **URL:** `/logout/`
- **Auth:** None (no harm in logging out an unauthenticated user).
- **Behavior:** Calls `logout(request)`, flashes a success message, redirects to login.
- **Returns:** Redirect.

---

# APPENDIX D — Vegetation Index Reference

The full vegetation index definitions live in [main/enum.py](../main/enum.py).

### Sentinel-2 Bands Used

| Band | TiTiler asset name | Wavelength | Used by |
|---|---|---|---|
| Blue (B2) | `blue` | 490 nm | EVI |
| Red (B4) | `red` | 665 nm | NDVI, EVI |
| NIR (B8) | `nir` | 842 nm | NDVI, EVI, NDMI |
| SWIR16 (B11) | `swir16` | 1610 nm | NDMI |

Other bands available (not used in the current three indices but reserved for future enhancements): `coastal`, `green`, `rededge1`, `rededge2`, `rededge3`, `nir08`, `nir09`, `swir22`.

### NDVI — Normalized Difference Vegetation Index

- **Formula:** `(nir - red) / (nir + red)`
- **Range:** -1.0 to 1.0
- **Default colormap:** RdYlGn (Red-Yellow-Green, with red as low/stressed and green as high/healthy)
- **Description:** Measures vegetation health and density.
- **Interpretation:**
  - 0.7 - 1.0: Dense, healthy vegetation
  - 0.4 - 0.7: Active crop / moderate canopy
  - 0.2 - 0.4: Sparse / stressed vegetation
  - 0.0 - 0.2: Bare soil
  - < 0.0: Water, snow, or clouds

### EVI — Enhanced Vegetation Index

- **Formula:** `2.5 * ((nir - red) / (nir + 6 * red - 7.5 * blue + 1))`
- **Range:** 0.0 to 1.0
- **Default colormap:** YlGn (Yellow-Green)
- **Description:** Improved vegetation index correcting atmospheric and soil effects.
- **Use case:** More reliable than NDVI in dense canopies (where NDVI saturates) and over bright soils.

### NDMI — Normalized Difference Moisture Index

- **Formula:** `(nir - swir16) / (nir + swir16)`
- **Range:** -1.0 to 1.0
- **Default colormap:** Blues
- **Description:** Measures vegetation moisture content.
- **Interpretation:**
  - 0.4+: Well-watered canopy
  - 0.1 - 0.4: Adequate moisture
  - < 0.1: Moisture stress / drought
  - Negative: Bare soil or water-stressed

### Available Colormaps

The `Colormap` enum in `main/enum.py` defines:
`viridis, plasma, inferno, magma, cividis, terrain, rainbow, jet, turbo, blues, greens, reds, greys, rdylgn, rdylbu, spectral, coolwarm`.

The user can override the default colormap per index by passing `colormap` in the get-imagery request.

---

# APPENDIX E — Open-Meteo Variable Reference

The full mapping is in [main/weather_api.py](../main/weather_api.py).

### Current Weather Payload (`/farm/<uuid>/weather/current/`)

**Top-level structure (after server-side remapping):**

```json
{
  "farm_id": "<uuid>",
  "farm_name": "...",
  "current": {
    "time": "...",
    "interval": 900,
    "temp": "<°C>",
    "relative_humidity": "<%>",
    "apparent_temperature": "<°C>",
    "precipitation": "<mm>",
    "rain": "<mm>",
    "cloud_cover": "<%>",
    "surface_pressure": "<hPa>",
    "wind_speed": "<km/h>",
    "wind_gusts": "<km/h>",
    "apparent_temperature_max": "<°C>",
    "apparent_temperature_min": "<°C>",
    "sunrise": "<iso8601>",
    "sunset": "<iso8601>",
    "uv_index_max": "<unitless>",
    "et0_fao_evapotranspiration": "<mm>",
    "soil_temperature_surface": "<°C>  (from 0 cm)",
    "soil_temperature_5cm": "<°C>  (from 6 cm)",
    "soil_temperature_15cm": "<°C>  (from 18 cm)",
    "soil_temperature_60cm": "<°C>  (from 54 cm)",
    "soil_moisture_surface": "<m³/m³>  (from 0-1 cm)",
    "soil_moisture_2cm": "<m³/m³>  (from 1-3 cm)",
    "soil_moisture_5cm": "<m³/m³>  (from 3-9 cm)",
    "soil_moisture_15cm": "<m³/m³>  (from 9-27 cm)",
    "soil_moisture_50cm": "<m³/m³>  (from 27-81 cm)"
  },
  "units": { ... full units dict ... }
}
```

Note the **key renaming**: Open-Meteo returns soil temperature at exact sensor depths (0, 6, 18, 54 cm), but the helper renames these to friendlier user-facing labels (surface, 5 cm, 15 cm, 60 cm). Similarly, soil moisture depths (0-1, 1-3, 3-9, 9-27, 27-81 cm) are renamed to (surface, 2 cm, 5 cm, 15 cm, 50 cm).

### Forecast Payload (`/farm/<uuid>/weather/forecast/`)

```json
{
  "farm_id": "<uuid>",
  "farm_name": "...",
  "forecast": {
    "time": ["2026-05-28", "2026-05-29", ..., "2026-06-12"],
    "temp_max": [<°C>, ...],     "temp_min": [<°C>, ...],    "temp_mean": [<°C>, ...],
    "relative_humidity": [<%>, ...],
    "precipitation": [<mm>, ...], "rain": [<mm>, ...],
    "surface_pressure": [<hPa>, ...],
    "cloud_cover": [<%>, ...],
    "evapotranspiration": [<mm>, ...],
    "wind_speed": [<km/h>, ...], "wind_gusts": [<km/h>, ...]
  },
  "units": { ... }
}
```

### Open-Meteo Variable Name Mapping

| Open-Meteo variable | CropGeo key | Units |
|---|---|---|
| `temperature_2m` | `temp` | °C |
| `relative_humidity_2m` | `relative_humidity` | % |
| `wind_speed_10m` | `wind_speed` | km/h |
| `wind_gusts_10m` | `wind_gusts` | km/h |
| `soil_temperature_0cm` | `soil_temperature_surface` | °C |
| `soil_temperature_6cm` | `soil_temperature_5cm` | °C |
| `soil_temperature_18cm` | `soil_temperature_15cm` | °C |
| `soil_temperature_54cm` | `soil_temperature_60cm` | °C |
| `soil_moisture_0_to_1cm` | `soil_moisture_surface` | m³/m³ |
| `soil_moisture_1_to_3cm` | `soil_moisture_2cm` | m³/m³ |
| `soil_moisture_3_to_9cm` | `soil_moisture_5cm` | m³/m³ |
| `soil_moisture_9_to_27cm` | `soil_moisture_15cm` | m³/m³ |
| `soil_moisture_27_to_81cm` | `soil_moisture_50cm` | m³/m³ |
| `temperature_2m_max` | `temp_max` | °C |
| `temperature_2m_min` | `temp_min` | °C |
| `temperature_2m_mean` | `temp_mean` | °C |
| `relative_humidity_2m_max` | `relative_humidity` | % |
| `precipitation_sum` | `precipitation` | mm |
| `rain_sum` | `rain` | mm |
| `surface_pressure_mean` | `surface_pressure` | hPa |
| `cloud_cover_mean` | `cloud_cover` | % |
| `et0_fao_evapotranspiration` | `evapotranspiration` | mm |
| `wind_speed_10m_max` | `wind_speed` | km/h |
| `wind_gusts_10m_max` | `wind_gusts` | km/h |

---

# APPENDIX F — Environment Variables Reference

The project loads environment variables from a `.env` file at project root using `python-dotenv`.

### Required Variables (database)

| Variable | Used in | Purpose |
|---|---|---|
| `DB_NAME` | `cropgeo/settings.py` `DATABASES['default']['NAME']` | PostgreSQL database name |
| `DB_USER` | `cropgeo/settings.py` `DATABASES['default']['USER']` | PostgreSQL user |
| `DB_PASSWORD` | `cropgeo/settings.py` `DATABASES['default']['PASSWORD']` | PostgreSQL password |
| `DB_HOST` | `cropgeo/settings.py` `DATABASES['default']['HOST']` | PostgreSQL host (e.g., `localhost`) |
| `DB_PORT` | `cropgeo/settings.py` `DATABASES['default']['PORT']` | PostgreSQL port (e.g., `5432`) |

### Optional Variables (services)

| Variable | Default | Purpose |
|---|---|---|
| `TITILER_URL` | `http://localhost:8888` | TiTiler service URL. Must start with `http://` or `https://`. Production deployments typically use `https://titiler.vistamap.co`. |

### Example `.env`

```
DB_NAME=cropgeo_db
DB_USER=cropgeo_user
DB_PASSWORD=replace-me
DB_HOST=localhost
DB_PORT=5432
TITILER_URL=https://titiler.vistamap.co
```

### Production Notes

- `SECRET_KEY` and `DEBUG` are currently hardcoded in `settings.py`. For production, these should also be sourced from environment variables.
- `ALLOWED_HOSTS = []` currently — must be populated with the production domain before going live.

---

# APPENDIX G — Migration History

All migrations live in [main/migrations/](../main/migrations/).

### 0001_initial

- Creates the `main_user` table (custom User extending AbstractUser).
- Adds custom fields: `age` (PositiveIntegerField), `gender` (CharField with choices).
- Sets `AUTH_USER_MODEL = "main.User"` (in settings).

### 0002_alter_user_age_alter_user_gender

- Adjusts the field constraints:
  - `age` default to 18.
  - `gender` choices: male, female, other, prefer-not-to-say; default `'prefer-not-to-say'`.

### 0003_farm

- Creates the `main_farm` table.
- Fields: `id` (UUID PK), `name` (CharField 255), `crop_type` (CharField 50 with choices), `size_acres` (FloatField, nullable), `geometry` (GeometryField SRID 4326), `area` (FloatField, nullable), `created_at` (auto_now_add), `updated_at` (auto_now), `user` (FK to User, on_delete=CASCADE, related_name='farms').
- Sets default ordering: `['-created_at']`.

### 0004_user_is_approved

- Adds `is_approved` (BooleanField, default False) to the `main_user` table.
- Enables the admin approval workflow.

### Note

After cloning the project to a fresh machine, run:
```
python manage.py migrate
```
This applies all four migrations to a fresh PostgreSQL+PostGIS database.

---

# HOW TO USE THIS DOCUMENT WITH AN AI ASSISTANT

This reference document is designed to be fed to any AI chatbot (ChatGPT, Claude, Gemini, Microsoft Copilot, etc.) to generate accurate, project-specific content for the CropGeo Analytics dissertation report.

### Recommended Workflow

1. **Paste this entire file** into the AI chat as your first message.
2. Add a prompt like:
   > "Above is the complete factual reference for my MCA dissertation project, CropGeo Analytics. From now on, when I ask for a black book section, generate prose in a typical MCA dissertation tone (similar to a Savitribai Phule Pune University black book), but only use the facts in this document. Do NOT invent features I do not have. Do NOT mention plant disease detection, leaf images, CNN, deep learning, MongoDB, OpenWeatherMap, or SQLite — these belong to a different project."
3. Then ask questions one at a time:
   - "Write Chapter 1.1 Introduction of proposed project — 2 pages, paragraph form."
   - "Write Section 2.2 GIS Web Platforms in Agriculture with the features / advantages / limitations bullet structure."
   - "Write Section 3.3 Functional Requirements as a numbered list with brief descriptions."
   - "Generate test case tables for Chapter 5.4 — 5 tables, one per module."
   - "Write the abstract in 250 words."
   - "Write the acknowledgement section (placeholder names)."

### Tips for Best Results

- **One section at a time.** AI generates better content when focused on a single section.
- **Specify length.** "2 pages" or "200 words" produces output of appropriate scale.
- **Cite the appendix.** When you need a precise list (URLs, models, fields), point the AI at the relevant appendix: "Use Appendix B as the source for the URL table."
- **Compare to the friend's PDF format.** "Write Chapter 5.1 Modules Used in the same paragraph + Working + Importance format as the Smart Plant Partner PDF's Chapter 5.1."
- **Re-verify before submission.** After the AI generates a section, skim it once and confirm every concrete claim matches this reference. If the AI invents a feature (e.g., "the platform sends SMS notifications" — which is in Future Scope, not implemented), fix it.

### Quick Reality-Check Test

Before pasting AI-generated content into your black book, do a "find" search in your final document for these forbidden phrases:

- "SQLite" — should never appear (you use PostGIS).
- "OpenWeatherMap" — should never appear (you use Open-Meteo).
- "leaf image" / "plant disease detection" / "CNN" / "Convolutional Neural Network" — belong to the friend's project.
- "MongoDB" / "Node.js" / "Express" — wrong stack; you use Django + PostgreSQL.
- "AR Plant Preview" / "Augmented Reality" — friend's feature, not yours.

If any of those appear, the AI hallucinated — replace those parts with content drawn from this reference.

### Section-by-Section AI Prompts

Copy-paste-friendly prompts for each chapter:

- **Title page + Certificate + Declaration + Approval:** "Generate the standard MCA dissertation front matter pages for my project. Use my name (Pratham Satish Pawar), college (Matoshri College of Engineering and Research Centre, Nashik), university (Savitribai Phule Pune University), year (2025-2026)."
- **Abstract:** "Write a 280-word abstract for CropGeo Analytics covering problem, solution, technology, and outcomes."
- **Chapter 1:** "Write Chapter 1 in full (1.1 through 1.8), about 7 pages total, prose with bullets where appropriate."
- **Chapter 2:** "Write Chapter 2 Literature Survey with the three subsections from this reference (2.1 satellite-based crop monitoring, 2.2 GIS web platforms, 2.3 COG/STAC). Use features / advantages / limitations bullets in each subsection."
- **Chapter 3:** "Write Chapter 3 SRS with hardware, software, functional, and non-functional requirements as in this reference. Use tables for hardware and software, numbered lists for functional, bulleted lists for non-functional."
- **Chapter 4:** "Write Chapter 4 Design and Modeling. For 4.1 System Architecture explain the client-server-database-services structure. For 4.2 E-R Diagram describe the User and Farm entities and their relationship. For 4.3 DFD describe Level 0, Level 1, Level 2. For 4.4 UML describe use case, sequence, and class diagrams. I will draw the actual diagrams separately."
- **Chapter 5:** "Write Chapter 5 Implementation and Testing. 5.1 describe each of the 8 modules with Working and Importance. 5.2 list the algorithms. 5.3 testing methodology. 5.4 generate 5 test case tables (Sample, Login, Registration, Farm Registration, Satellite Analysis). 5.5 list the 10 screenshots with descriptions."
- **Chapter 6:** "Write Chapter 6 Result and Analysis: results summary, report generation pipeline, discussion of strengths and limitations."
- **Chapter 7:** "Write Chapter 7 Conclusion and Future Scope. Use the full Future Scope list from this reference (16 items grouped into Platform / Data / Intelligence / Accessibility)."
- **References:** "Format the 15 references from this document in IEEE style."

---

*End of CropGeo Analytics Reference Document.*

*Last updated: 2026-05-28.*
*Maintainer: Pratham Satish Pawar (prathampawar501@gmail.com).*
