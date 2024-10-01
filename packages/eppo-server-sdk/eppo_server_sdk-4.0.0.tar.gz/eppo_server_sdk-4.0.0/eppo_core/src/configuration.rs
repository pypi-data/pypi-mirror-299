use std::collections::HashMap;

use chrono::{DateTime, Utc};

use crate::{
    bandits::{BanditConfiguration, BanditResponse},
    ufc::{BanditVariation, TryParse, UniversalFlagConfig},
};

/// Remote configuration for the eppo client. It's a central piece that defines client behavior.
#[derive(Clone)]
pub struct Configuration {
    /// Timestamp when configuration was fetched by the SDK.
    pub fetched_at: DateTime<Utc>,
    /// Flags configuration.
    pub flags: UniversalFlagConfig,
    /// Bandits configuration.
    pub bandits: Option<BanditResponse>,
    /// Mapping from flag key to flag variation value to bandit variation. Cached from
    /// `self.flags.bandits`.
    pub flag_to_bandit_associations:
        HashMap</* flag_key: */ String, HashMap</* variation_key: */ String, BanditVariation>>,
}

impl Configuration {
    /// Create a new configuration from server responses.
    pub fn from_server_response(
        config: UniversalFlagConfig,
        bandits: Option<BanditResponse>,
    ) -> Configuration {
        let now = Utc::now();

        // warn if some flags failed to parse
        for (name, flag) in &config.flags {
            if let TryParse::ParseFailed(_value) = flag {
                log::warn!(target: "eppo", "failed to parse flag configuration: {name:?}");
            }
        }

        let flag_to_bandit_associations = get_flag_to_bandit_associations(&config);

        Configuration {
            fetched_at: now,
            flags: config,
            bandits,
            flag_to_bandit_associations,
        }
    }

    /// Return a bandit variant for the specified flag key and string flag variation.
    pub(crate) fn get_bandit_key<'a>(&'a self, flag_key: &str, variation: &str) -> Option<&'a str> {
        self.flag_to_bandit_associations
            .get(flag_key)
            .and_then(|x| x.get(variation))
            .map(|variation| variation.key.as_str())
    }

    /// Return bandit configuration for the given key.
    ///
    /// Returns `None` if bandits are missing for bandit does not exist.
    pub(crate) fn get_bandit<'a>(&'a self, bandit_key: &str) -> Option<&'a BanditConfiguration> {
        self.bandits.as_ref()?.bandits.get(bandit_key)
    }
}

fn get_flag_to_bandit_associations(
    config: &UniversalFlagConfig,
) -> HashMap<String, HashMap<String, BanditVariation>> {
    config
        .bandits
        .iter()
        .flat_map(|(_, bandits)| bandits.iter())
        .fold(HashMap::new(), |mut acc, variation| {
            acc.entry(variation.flag_key.clone())
                .or_default()
                .insert(variation.variation_value.clone(), variation.clone());
            acc
        })
}
