# Ugram iOS preview

Build bootstrap for a personal iPhone preview, based on the official
[Telegram-iOS release 13.2](https://github.com/TelegramMessenger/Telegram-iOS/tree/24638bc69bd083981b178dd1e7f921eebbf7fc46).
This is an unofficial client. The original bootstrap passed cloud build #2.
The new feature overlay below still requires its own successful cloud build and
device acceptance checks. This is not complete Android/iOS feature parity.

## Ugram feature preview

Open the **Ugram** tab to enable individual features. All switches default off;
switches apply to all accounts on this device, while archives are account-local.

| Feature | Implementation and limits |
| --- | --- |
| Deleted messages | Snapshots messages already stored locally before live server deletion updates; separate history screen, also accessible from a chat's message menu. |
| Edit history | Retains the previous locally stored version before an edit update. |
| Deleted media | Keeps a hard-linked/copied version of fully downloaded media outside Telegram's cache. Missing downloads are explicitly labelled; no server recovery. |
| Share as copy | Message-menu action downloads one selected image/file and creates a new upload with its media attributes. Supports ordinary and round video, voice, music, documents, GIFs and stickers; native destination permissions remain enforced. Multi-item album reconstruction is not implemented. |
| Ghost mode | Separate switches for read receipts, story views, typing and online status. Local operation cleanup continues; no fake server pts. Other sessions can still reveal activity. Turning reads back on can reveal earlier reads through subsequent cumulative read watermarks. |
| Local content rules | Optional relaxation of non-sensitive client restriction rules. Server access, paid content and age checks remain intact. |
| Regex filter | Hides matching incoming messages locally; bounded pattern/input and matching time. Reopen the chat after changing it. Does not delete messages. |
| Message details / translation | Message IDs, sender, date and file information. Explicit actions open Google Translate (Uzbek) or DeepL (English) in the browser; the selected text is shared only when the user chooses that action. Native Telegram translation remains available. |

History excludes secret chats, self-destructing/timed/ephemeral, paid and age-gated
content. It cannot recover content never received or downloaded. Cleanup during
offline history-gap recovery is not currently archived. History retains at most
5,000 records and 1 GB of media, evicting the oldest first. It stays in the app's
account container, is excluded from backup, and can be cleared in Ugram settings.
Android-only appearance/Monet, UnifiedPush, arbitrary API/DNS settings and local
Premium UI emulation are not part of this iOS preview.

The complete auditable source diff is `ugram.patch`; `scripts/apply_features.py`
checks every hunk before applying it. `overlay/`, `tests/` and the patch generator
are maintained in the local development workspace; the public build repository
needs only the resulting patch and build scripts. The patch includes host Swift
tests for durable media retention, Unicode, account/chat isolation, path safety,
limits, feature toggles and filters, plus a parse check for new Swift files.
An actual iOS build and device checks are still required for Telegram integration.

## Free build from Linux

1. Put only the contents of this `ios` directory in a new public GitHub repository.
   Do not upload the parent Android workspace, signing keys, or local configuration.
2. Create your own application at https://my.telegram.org/apps.
3. In the new repository, open **Settings → Secrets and variables → Actions**.
   Add repository secrets `TELEGRAM_API_ID` and `TELEGRAM_API_HASH`.
   Do not put these values in source files, workflow inputs, issues, or chat.
4. Open **Actions → iPhone preview → Run workflow**.
   For personal testing with the published API already used by an Android build,
   enable **Allow the published Android API for personal testing only**. This is
   off by default. Telegram's sample API is server-limited and is unsuitable for
   distributing an app; obtain your own API before distribution. See
   [Telegram's API guide](https://core.telegram.org/api/obtaining_api_id).
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

Device acceptance: install the new build, enable the needed switches, then use
two test accounts to exercise deletion/edit while the app is online, downloaded
and missing media, relaunch persistence, copy/upload and cancellation, each ghost
toggle on/off, account switching, filtering and clearing history. No device test
is claimed until these are performed. Native UIKit screens also need visual QA
on an iPhone; the Linux workspace cannot record an iOS simulator.

References: [GitHub runner images](https://github.com/actions/runner-images),
[Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions),
[Apple free-account limits](https://developer.apple.com/help/account/basics/about-your-developer-account/).
