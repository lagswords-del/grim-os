// Grim Browser: settings for the Grim profile (copied into it on every start, so updates apply).
// Firefox underneath, with no telemetry, no data to Mozilla/Google/anyone, and fingerprinting
// protection on. Change things in Grim Shield's settings page, not here.

// ---------------------------------------------------------------- no telemetry or data collection
user_pref("toolkit.telemetry.enabled", false);
user_pref("toolkit.telemetry.unified", false);
user_pref("toolkit.telemetry.archive.enabled", false);
user_pref("toolkit.telemetry.server", "data:,");
user_pref("toolkit.telemetry.newProfilePing.enabled", false);
user_pref("toolkit.telemetry.shutdownPingSender.enabled", false);
user_pref("toolkit.telemetry.updatePing.enabled", false);
user_pref("toolkit.telemetry.bhrPing.enabled", false);
user_pref("toolkit.telemetry.firstShutdownPing.enabled", false);
user_pref("toolkit.telemetry.coverage.opt-out", true);
user_pref("toolkit.coverage.opt-out", true);
user_pref("toolkit.coverage.endpoint.base", "");
user_pref("datareporting.healthreport.uploadEnabled", false);
user_pref("datareporting.policy.dataSubmissionEnabled", false);
user_pref("datareporting.usage.uploadEnabled", false);
user_pref("app.shield.optoutstudies.enabled", false);
user_pref("app.normandy.enabled", false);
user_pref("app.normandy.api_url", "");
user_pref("breakpad.reportURL", "");
user_pref("browser.tabs.crashReporting.sendReport", false);
user_pref("browser.crashReports.unsubmittedCheck.autoSubmit2", false);
user_pref("browser.ping-centre.telemetry", false);
user_pref("browser.newtabpage.activity-stream.feeds.telemetry", false);
user_pref("browser.newtabpage.activity-stream.telemetry", false);
user_pref("beacon.enabled", false);
user_pref("browser.send_pings", false);
user_pref("dom.private-attribution.submission.enabled", false);   // "privacy-preserving" ad measurement: off

// ---------------------------------------------------------------- nothing sponsored, suggested or recommended
user_pref("browser.newtabpage.activity-stream.showSponsored", false);
user_pref("browser.newtabpage.activity-stream.showSponsoredTopSites", false);
user_pref("browser.newtabpage.activity-stream.feeds.section.topstories", false);
user_pref("browser.newtabpage.activity-stream.feeds.topsites", false);
user_pref("browser.urlbar.quicksuggest.enabled", false);
user_pref("browser.urlbar.suggest.quicksuggest.sponsored", false);
user_pref("browser.urlbar.suggest.quicksuggest.nonsponsored", false);
user_pref("browser.urlbar.suggest.trending", false);
user_pref("browser.urlbar.trending.featureGate", false);
user_pref("browser.urlbar.suggest.weather", false);
user_pref("browser.urlbar.suggest.yelp", false);
user_pref("browser.urlbar.suggest.addons", false);
user_pref("browser.urlbar.suggest.mdn", false);
user_pref("browser.urlbar.suggest.pocket", false);
user_pref("browser.search.suggest.enabled", false);          // typing in the bar doesn't go to a search engine
user_pref("browser.discovery.enabled", false);
user_pref("extensions.getAddons.showPane", false);
user_pref("extensions.htmlaboutaddons.recommendations.enabled", false);
user_pref("browser.newtabpage.activity-stream.asrouter.userprefs.cfr.addons", false);
user_pref("browser.newtabpage.activity-stream.asrouter.userprefs.cfr.features", false);
user_pref("extensions.pocket.enabled", false);
user_pref("browser.ml.enable", false);                          // built-in AI features
user_pref("browser.ml.chat.enabled", false);
user_pref("identity.fxaccounts.enabled", false);                // Firefox accounts / Sync (Mozilla servers)

// ---------------------------------------------------------------- no background calls home
user_pref("browser.safebrowsing.malware.enabled", false);       // Safe Browsing downloads lists from Google
user_pref("browser.safebrowsing.phishing.enabled", false);
user_pref("browser.safebrowsing.downloads.enabled", false);
user_pref("browser.safebrowsing.downloads.remote.enabled", false);
user_pref("browser.safebrowsing.provider.google4.updateURL", "");
user_pref("browser.safebrowsing.provider.google.updateURL", "");
user_pref("network.captive-portal-service.enabled", false);     // detectportal.firefox.com
user_pref("network.connectivity-service.enabled", false);
user_pref("geo.provider.network.url", "");                      // location lookups
user_pref("geo.provider.use_geoclue", false);
user_pref("browser.region.network.url", "");
user_pref("browser.region.update.enabled", false);
user_pref("browser.search.update", false);
user_pref("app.update.auto", false);                            // updates come from xbps / pacman
user_pref("dom.push.enabled", false);                           // push needs a Mozilla server connection
user_pref("network.prefetch-next", false);
user_pref("network.dns.disablePrefetch", true);
user_pref("network.predictor.enabled", false);
user_pref("network.http.speculative-parallel-limit", 0);
user_pref("browser.places.speculativeConnect.enabled", false);
user_pref("browser.urlbar.speculativeConnect.enabled", false);
user_pref("media.gmp-gmpopenh264.autoupdate", false);           // Cisco's codec download
user_pref("media.gmp-manager.url", "data:text/plain,");
user_pref("extensions.blocklist.enabled", true);                // keep: Mozilla's list of malicious add-ons
user_pref("browser.startup.homepage_override.mstone", "ignore");
user_pref("startup.homepage_welcome_url", "");
user_pref("startup.homepage_override_url", "");
user_pref("browser.aboutwelcome.enabled", false);
user_pref("browser.shell.checkDefaultBrowser", false);
user_pref("trailhead.firstrun.didSeeAboutWelcome", true);
user_pref("datareporting.policy.firstRunURL", "");

// ---------------------------------------------------------------- tracking protection
user_pref("browser.contentblocking.category", "strict");
user_pref("privacy.trackingprotection.enabled", true);
user_pref("privacy.trackingprotection.socialtracking.enabled", true);
user_pref("privacy.query_stripping.enabled", true);            // strips tracking bits from links
user_pref("privacy.globalprivacycontrol.enabled", true);       // tells sites "don't sell my data"
user_pref("network.cookie.cookieBehavior", 5);                  // cookies kept per site (Total Cookie Protection)
user_pref("network.http.referer.XOriginTrimmingPolicy", 2);
user_pref("dom.security.https_only_mode", true);
user_pref("dom.security.https_only_mode_send_http_background_request", false);

// ---------------------------------------------------------------- fingerprinting
// resistFingerprinting reports a common, generic profile: a standard screen size (letterboxing),
// UTC time zone, English, a US keyboard layout, a common OS and fewer hardware details.
user_pref("privacy.resistFingerprinting", true);
user_pref("privacy.resistFingerprinting.letterboxing", true);
user_pref("privacy.resistFingerprinting.block_mozAddonManager", true);
user_pref("privacy.spoof_english", 2);
user_pref("privacy.fingerprintingProtection", true);
user_pref("media.peerconnection.ice.default_address_only", true);   // WebRTC can't leak your IP
user_pref("media.peerconnection.ice.no_host", true);
user_pref("media.peerconnection.ice.proxy_only_if_behind_proxy", true);
user_pref("webgl.disabled", false);                               // RFP already blurs WebGL; off breaks maps
user_pref("dom.battery.enabled", false);
user_pref("device.sensors.enabled", false);

// ---------------------------------------------------------------- private windows
user_pref("network.proxy.socks_remote_dns", true);               // with Tor, DNS goes through Tor too
user_pref("browser.privatebrowsing.vpnpromourl", "");
user_pref("browser.privatebrowsing.enable-new-indicator", false);

// ---------------------------------------------------------------- Grim
user_pref("extensions.autoDisableScopes", 0);                   // Grim Shield (system add-on) starts enabled
user_pref("extensions.enabledScopes", 15);
user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);   // userChrome.css (transparency)
user_pref("browser.tabs.allow_transparent_browser", true);
user_pref("browser.startup.page", 1);
user_pref("browser.download.useDownloadDir", false);            // ask where to save
user_pref("browser.tabs.firefox-view", false);
user_pref("browser.toolbars.bookmarks.visibility", "never");
