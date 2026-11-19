# Ugram iOS preview

Build bootstrap for a personal iPhone preview, based on the official
[Telegram-iOS release 13.2](https://github.com/TelegramMessenger/Telegram-iOS/tree/24638bc69bd083981b178dd1e7f921eebbf7fc46).
This is an unofficial client. **The Android Ugram features have not been ported.**
The bootstrap has not yet passed a macOS build or an iPhone installation test.

## Free build from Linux

1. Put only the contents of this `ios` directory in a new public GitHub repository.
   Do not upload the parent Android workspace, signing keys, or local configuration.
2. Create your own application at https://my.telegram.org/apps.
3. In the new repository, open **Settings → Secrets and variables → Actions**.
   Add repository secrets `TELEGRAM_API_ID` and `TELEGRAM_API_HASH`.
   Do not put these values in source files, workflow inputs, issues, or chat.
4. Open **Actions → iPhone preview → Run workflow**.
5. Download the `Ugram-iOS-preview` artifact and extract `Ugram-preview.ipa`.

The workflow uses the standard `xcode-27` GitHub-hosted runner and deliberately
does not run in a private repository. Standard runners for public repositories
are free. It runs only on manual dispatch, uploads no release, uses no paid
runner, and keeps artifacts for 3 days. Availability and successful compilation
still need to be confirmed by the first run.

The source is pinned in `upstream.json`. Xcode 27.1 is required by that source;
the target phone does not need to run the same version as the build SDK.
All upstream license notices remain in the fetched checkout. Telegram source
is licensed under GPL; see the upstream LICENSE and individual dependencies.

## iPhone 15 Pro / iOS 26.2: installation from Ubuntu

Follow the [official SideStore instructions](https://docs.sidestore.io/docs/installation/prerequisites).
Use the stable [iloader](https://iloader.app/) Linux release, a USB data cable,
and a free Apple Account. `usbmuxd` must be installed on Ubuntu.

1. On iPhone, install LocalDevVPN from the App Store as linked by SideStore.
2. Connect iPhone by USB, unlock it, and trust the computer when prompted.
3. Open iloader, sign in to your Apple Account there, select the phone, and choose
   **Install SideStore (Stable)**. Passwords and 2FA codes stay out of this repository.
4. Follow the on-device trust and **Developer Mode** steps from the
   [installation guide](https://docs.sidestore.io/docs/installation/install).
5. Connect LocalDevVPN, open SideStore, use the same Apple Account, and refresh
   SideStore once. Import the generated `Ugram-preview.ipa` to sign and install it.
6. Refresh the apps before their 7-day signatures expire. SideStore needs Wi-Fi
   and LocalDevVPN during refresh. A free account has a 3-app installation limit;
   SideStore itself occupies one slot.

The downloaded IPA has only an ad-hoc placeholder signature. It is **not directly
installable** until iloader/SideStore signs it for your account and device.
Extensions, Siri, iCloud, and Watch are disabled in this first preview. Push
notifications and background delivery are not validated and must not be assumed
to work. First test login, messages, reopening the app, then refresh and relaunch.

## Local preparation and status

`scripts/prepare.py` validates the pinned source and prepares build configuration
without printing API values. `scripts/build.sh` runs only on macOS.
`scripts/package.py` verifies an iPhone archive and embeds minimal entitlements
for the subsequent local signing step. `scripts/icon.swift` draws a placeholder
Ugram icon. None of these scripts access an Apple account.

Next milestones: first successful cloud build, successful sideload and login,
then an explicit implementation and device test of each Ugram-specific feature.

References: [GitHub runner images](https://github.com/actions/runner-images),
[Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions),
[Apple free-account limits](https://developer.apple.com/help/account/basics/about-your-developer-account/).
