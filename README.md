# Awesome Moodle [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A curated list of Moodle plugins, themes, tools, and learning resources for educators, administrators, and developers.

[![Moodle 5.3 LTS](https://img.shields.io/badge/Moodle-5.3%20LTS-f98012.svg)](https://moodledev.io/general/releases/5.3)
[![Contributors](https://img.shields.io/github/contributors/moosensei/awesome-moodle.svg)](https://github.com/moosensei/awesome-moodle/graphs/contributors)
[![Last Commit](https://img.shields.io/github/last-commit/moosensei/awesome-moodle.svg)](https://github.com/moosensei/awesome-moodle/commits/main)
[![License: CC0-1.0](https://img.shields.io/badge/License-CC0%201.0-lightgrey.svg)](LICENSE)
[![Submit a resource](https://img.shields.io/badge/Submit-a%20resource-brightgreen.svg)](https://github.com/moosensei/awesome-moodle/issues/new?template=add-resource.yml)

![Awesome Moodle](https://i.postimg.cc/1zd3ML6F/awesome-moodle-hero-banner.jpg)

Moodle is the most widely used open-source learning platform in the world. This list collects the plugins, themes, tools, and learning resources worth knowing, from the first course to a production deployment. Plugins and services are marked ![Free](https://img.shields.io/badge/Free-green) or ![Premium](https://img.shields.io/badge/Premium-orange).

**Know something that belongs here?** [Submit it through the form](https://github.com/moosensei/awesome-moodle/issues/new?template=add-resource.yml): a bot checks it and opens a pull request for review. See [Contributing](#-contributing). Questions: [madewithmoodle@gmail.com](mailto:madewithmoodle@gmail.com).

## 🚀 Quick Start

New to Moodle? Start here.

- 🎯 [Moodle Sandbox](https://sandbox.moodledemo.net/) - Try Moodle in the browser without installing anything. The demo site is reset regularly, so experiment freely.
- 📖 [Teacher Quick Guide](https://docs.moodle.org/en/Teacher_quick_guide) - Create a first course, add activities, and enrol students step by step.
- 🎓 [Moodle Academy](https://moodle.academy/) - Free official courses for educators, administrators, and developers.

## 📋 Contents

- [🏛️ Official](#%EF%B8%8F-official)
- [🔌 Plugins](#-plugins)
  - [📚 Content & Activities](#-content--activities)
  - [🎨 Course Design](#-course-design)
  - [📊 Analytics & Reports](#-analytics--reports)
  - [🔐 Authentication & Security](#-authentication--security)
  - [🤖 AI & Machine Learning](#-ai--machine-learning)
  - [📱 Mobile & Accessibility](#-mobile--accessibility)
  - [🎮 Gamification](#-gamification)
  - [💬 Communication](#-communication)
  - [📝 Assessment & Testing Enhancements](#-assessment--testing-enhancements)
- [🔗 Integrations & External Systems](#-integrations--external-systems)
- [🎨 Themes](#-themes)
- [⚡ Development](#-development)
- [🛠️ Tools & Utilities](#%EF%B8%8F-tools--utilities)
- [☁️ Hosting & Services](#%EF%B8%8F-hosting--services)
- [🚚 Migration to Moodle](#-migration-to-moodle)
- [🚀 Versions & Releases](#-versions--releases)
- [📚 Tutorials & Guides](#-tutorials--guides)
- [🎓 Courses & Learning](#-courses--learning)
- [🎥 Videos & Channels](#-videos--channels)
- [📖 Books & Publications](#-books--publications)
- [👥 Community](#-community)
- [🌍 Conferences & Events](#-conferences--events)
- [💼 Jobs & Careers](#-jobs--careers)
- [🌐 Multilingual Resources](#-multilingual-resources)
- [📢 News & Ecosystem Updates (2025–2026)](#-news--ecosystem-updates-20252026)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)

## 🏛️ Official

Resources maintained by Moodle HQ: the authoritative source for documentation, releases, and plugins.

- 🌐 [Moodle.org](https://moodle.org/) - The community site with forums, news, and downloads.
- 📖 [Moodle Documentation](https://docs.moodle.org/) - User and administrator documentation for every supported Moodle version.
- 👨‍💻 [Moodle Developer Resources](https://moodledev.io/) - Developer documentation: APIs, plugin types, coding style, and the development process.
- 🎓 [Moodle Academy](https://moodle.academy/) - Free courses and learning paths for educators, administrators, and developers, with official badges.
- 📦 [Moodle on GitHub](https://github.com/moodle/moodle) - The official source code repository.
- 📋 [Release Information](https://moodledev.io/general/releases) - Release dates, support periods, and LTS versions for every Moodle branch.
- ⬇️ [Downloads](https://download.moodle.org/releases/latest/) - Official packages of the latest and previous Moodle releases.
- 🗺️ [Roadmap](https://moodledev.io/general/community/roadmap) - Planned projects and features for upcoming releases.
- 📊 [Statistics](https://stats.moodle.org/) - Registered Moodle sites and users worldwide. As of 2026, Moodle reports more than 500 million users on over 148,000 registered sites.
- 🛒 [Moodle Marketplace](https://marketplace.moodle.com/) - The official home of Moodle plugins since mid-2026, replacing the plugins directory; it lists free and paid plugins and handles payments.
- 🤖 [AI Tools Documentation](https://docs.moodle.org/en/AI_tools) - Moodle's built-in AI subsystem (since 4.5): placements, actions, and providers such as OpenAI, Azure AI, Ollama, Gemini, Amazon Bedrock, and, since 5.3, Anthropic Claude.
- 🏢 [Moodle Workplace](https://moodle.com/products/workplace/) - Moodle HQ's edition for corporate learning, built on Moodle LMS, with multi-tenancy, programs, certifications, and learning catalogues.
- 🌐 [Moodle Events](https://moodle.com/events/) - Official calendar of MoodleMoots and virtual events, including MIX (Moodle Ideas Exchange), the flagship conference formerly called MoodleMoot Global.

[🔝 Back to top](#-contents)

## 🔌 Plugins

Community-developed and commercial plugins that extend Moodle. Most are listed in the [Moodle Marketplace](https://marketplace.moodle.com/); check that a plugin supports your Moodle version before installing it.

### 📚 Content & Activities

Interactive content and activity types for richer courses.

- 🎮 [H5P](https://h5p.org/moodle) ![Free](https://img.shields.io/badge/Free-green) - Interactive HTML5 content such as interactive videos, quizzes, and presentations. Moodle has a built-in H5P activity since 3.9.
- 📹 [BigBlueButton](https://marketplace.moodle.com/plugins/mod_bigbluebuttonbn) ![Free](https://img.shields.io/badge/Free-green) - Web conferencing for live classes, with recordings and breakout rooms. Part of Moodle core since 4.0.
- 📝 [Questionnaire](https://marketplace.moodle.com/plugins/mod_questionnaire) ![Free](https://img.shields.io/badge/Free-green) - Surveys with many question types and branching logic for feedback and research.
- 🎬 [VideoTime](https://marketplace.moodle.com/plugins/mod_videotime) ![Free](https://img.shields.io/badge/Free-green) - Embeds Vimeo and YouTube videos with viewing statistics and completion tracking.
- 📅 [Scheduler](https://marketplace.moodle.com/plugins/mod_scheduler) ![Free](https://img.shields.io/badge/Free-green) - Appointment booking for one-on-one meetings, office hours, and consultations.
- ✅ [Checklist](https://marketplace.moodle.com/plugins/mod_checklist) ![Free](https://img.shields.io/badge/Free-green) - Checklists that help students and teachers track learning objectives and course milestones.
- 🗳️ [Choice Group](https://marketplace.moodle.com/plugins/mod_choicegroup) ![Free](https://img.shields.io/badge/Free-green) - Lets students choose which group to join, for projects and collaborative work.
- 📱 [Student Folder](https://marketplace.moodle.com/plugins/mod_publication) ![Free](https://img.shields.io/badge/Free-green) - A shared folder where students upload files that teachers and classmates can view.
- 💻 [Virtual Programming Lab](https://marketplace.moodle.com/plugins/mod_vpl) ![Free](https://img.shields.io/badge/Free-green) - Programming assignments with in-browser editing, code execution, and automated evaluation.
- 📅 [Booking](https://marketplace.moodle.com/plugins/mod_booking) ![Free](https://img.shields.io/badge/Free-green) - Manages event bookings, registrations, and participant lists.
- 🛒 [Shopping Cart](https://marketplace.moodle.com/plugins/local_shopping_cart) ![Free](https://img.shields.io/badge/Free-green) - A shopping cart and checkout for selling courses and items inside Moodle.
- 🎲 [Gamoteca](https://www.gamoteca.com/) ![Free](https://img.shields.io/badge/Free-green) - A platform for building collaborative, game-based learning experiences and simulations.
- 🗺️ [Learning Map](https://marketplace.moodle.com/plugins/mod_learningmap) ![Free](https://img.shields.io/badge/Free-green) - Shows course activities as places on a map, with their completion state.
- 🛤️ [Programs (MuTMS)](https://marketplace.moodle.com/plugins/tool_muprog) ![Free](https://img.shields.io/badge/Free-green) - Learning programs across courses: define learning paths, automate enrolments, and track completion at scale.
- 🧭 [Adele Learning Path](https://wunderbyte.at/en/2025/10/01/adele-learning-path/) ![Free](https://img.shields.io/badge/Free-green) - Maps learning journeys by linking courses and activities into a guided path.
- 📚 [Wunderbyte Table](https://marketplace.moodle.com/plugins/local_wunderbyte_table) ![Free](https://img.shields.io/badge/Free-green) - A table library with templates, filtering, and search, used by other plugins to display data.
- 📥 [Download Center](https://marketplace.moodle.com/plugins/local_downloadcenter) ![Free](https://img.shields.io/badge/Free-green) - Lets students download all course files as one ZIP archive.
- 🔗 [Child Course](https://marketplace.moodle.com/plugins/mod_childcourse) ![Free](https://img.shields.io/badge/Free-green) - A "Linked course" activity that enrols users automatically and keeps groups and roles in sync between a parent and a child course.
- 🏅 [Navigatr](https://marketplace.moodle.com/plugins/local_navigatr) ![Free](https://img.shields.io/badge/Free-green) - Issues verifiable digital badges and certificates when learners complete courses.
- 🔄 [Drip Release](https://marketplace.moodle.com/plugins/tool_driprelease) ![Free](https://img.shields.io/badge/Free-green) - Releases course activities one after another on a schedule.
- 👥 [PlayerGroup](https://marketplace.moodle.com/plugins/mod_playergroup) ![Free](https://img.shields.io/badge/Free-green) - Students form groups and invite peers themselves, with privacy levels, automatic groupings, and gradebook integration.
- ⏰ [Late Penalty](https://marketplace.moodle.com/plugins/local_latepenalty) ![Free](https://img.shields.io/badge/Free-green) - Applies daily grade deductions to late submissions in any graded activity, with per-user overrides.
- 🧩 [Alphabet Wheel](https://github.com/OksigeniaSL/h5p-oksigenia) ![Free](https://img.shields.io/badge/Free-green) - H5P content type with one clue for each letter of the alphabet. Students type the answers or pass letters to a later round, and each finished game sends one point per letter to the Moodle gradebook. In eight languages.

### 🎨 Course Design

Course formats and page builders that change how a course looks and is navigated.

- 🖼️ [Edwiser Course Formats](https://edwiser.org/course-formats/) ![Premium](https://img.shields.io/badge/Premium-orange) - Card and list course layouts with progress indicators.
- 📱 [Tiles Format](https://marketplace.moodle.com/plugins/format_tiles) ![Free](https://img.shields.io/badge/Free-green) - Shows course sections as tiles that open in place.
- 🎪 [Onetopic Format](https://marketplace.moodle.com/plugins/format_onetopic) ![Free](https://img.shields.io/badge/Free-green) - Shows one section at a time, with tabs to move between sections.
- 🎯 [Grid Format](https://marketplace.moodle.com/plugins/format_grid) ![Free](https://img.shields.io/badge/Free-green) - Shows course sections as a grid of images.
- 📑 [Collapsed Topics](https://marketplace.moodle.com/plugins/format_topcoll) ![Free](https://img.shields.io/badge/Free-green) - Collapsible sections that keep long courses manageable.
- 🎨 [Edwiser Page Builder](https://edwiser.org/page-builder-for-moodle/) ![Premium](https://img.shields.io/badge/Premium-orange) - Drag-and-drop builder for course and site pages with ready-made blocks.
- 🌊 [Flexible Sections](https://marketplace.moodle.com/plugins/format_flexsections) ![Free](https://img.shields.io/badge/Free-green) - Nested sections for courses with a deep, hierarchical structure.
- 📋 [Board Format](https://marketplace.moodle.com/plugins/format_board) ![Free](https://img.shields.io/badge/Free-green) - Arranges sections in columns, like a board, for project-based courses.
- 🗂️ [Subsections](https://docs.moodle.org/en/Course_sections) ![Free](https://img.shields.io/badge/Free-green) - Built-in nested sections inside course sections, enabled by default since Moodle 5.0. In 5.2, subsection navigation uses anchor links instead of separate pages.

### 📊 Analytics & Reports

Reports and dashboards that show how students engage and who needs help.

- 📈 [Configurable Reports](https://marketplace.moodle.com/plugins/block_configurable_reports) ![Free](https://img.shields.io/badge/Free-green) - Builds custom reports, including SQL reports, without changing code.
- 🎯 [Learning Analytics](https://marketplace.moodle.com/plugins/local_learning_analytics) ![Free](https://img.shields.io/badge/Free-green) - Course dashboards with engagement metrics and learning patterns.
- ⚠️ [Solin Early Warning](https://marketplace.moodle.com/plugins/block_atrisk) ![Free](https://img.shields.io/badge/Free-green) - Shows teachers, inside the course, which students may be falling behind and why. Transparent, configurable signals over data Moodle already has, with no ML backend and no notification emails.
- 📊 [IntelliBoard](https://intelliboard.net/) ![Premium](https://img.shields.io/badge/Premium-orange) - Learning analytics and reporting platform with predictive analytics for at-risk students.
- 📈 [Progress Bar](https://marketplace.moodle.com/plugins/block_progress) ![Free](https://img.shields.io/badge/Free-green) - A visual bar of each student's progress through course activities.
- 🎓 [Completion Progress](https://marketplace.moodle.com/plugins/block_completion_progress) ![Free](https://img.shields.io/badge/Free-green) - Shows activity completion status at a glance for students and teachers.
- 📋 [Grade Overview](https://marketplace.moodle.com/plugins/block_grade_overview) ![Free](https://img.shields.io/badge/Free-green) - A block that summarizes grades for quick access.
- 📊 [Web Analytics](https://marketplace.moodle.com/plugins/tool_webanalytics) ![Free](https://img.shields.io/badge/Free-green) - Connects Moodle to Matomo, Google Tag Manager, and Google Analytics.
- 📊 [Resource Stats](https://marketplace.moodle.com/plugins/local_resourcestats) ![Free](https://img.shields.io/badge/Free-green) - Shows teachers view counts and unique students for each resource on the course page, with GDPR-compliant privacy support.
- ✅ [Teacher Checklist](https://marketplace.moodle.com/plugins/block_teacher_checklist) ![Free](https://img.shields.io/badge/Free-green) - Detects nine common course setup issues and keeps a manual to-do list, so a course is ready before students arrive.

### 🔐 Authentication & Security

Single sign-on, user directories, and login security.

- 🔑 [SAML2 SSO](https://marketplace.moodle.com/plugins/auth_saml2) ![Free](https://img.shields.io/badge/Free-green) - Single sign-on with institutional SAML identity providers.
- 🔐 [OAuth 2 Authentication](https://docs.moodle.org/en/OAuth_2_authentication) ![Free](https://img.shields.io/badge/Free-green) - Built-in login with Google, Microsoft, Facebook, or any OAuth 2 provider.
- 🏢 [LDAP](https://docs.moodle.org/en/LDAP_authentication) ![Free](https://img.shields.io/badge/Free-green) - Built-in LDAP and Active Directory authentication and user sync.
- 🔒 [Multi-Factor Authentication (MFA)](https://marketplace.moodle.com/plugins/tool_mfa) ![Free](https://img.shields.io/badge/Free-green) - Authenticator apps, security keys, SMS, and email codes. Part of Moodle core since 4.3; in 5.2 all MFA methods got a consistent new look.

### 🤖 AI & Machine Learning

AI providers and AI-powered tools. Since Moodle 4.5, a core AI subsystem connects Moodle to AI providers that plugins and placements share.

- 🧠 [Moodle Core AI](https://docs.moodle.org/en/AI_tools) ![Free](https://img.shields.io/badge/Free-green) - The built-in AI subsystem: providers such as OpenAI, Azure AI, and Ollama, and placements for generating and summarizing text and images.
- 💬 [OpenAI Chat Block](https://marketplace.moodle.com/plugins/block_openai_chat) ![Free](https://img.shields.io/badge/Free-green) - A course block with a configurable AI chat assistant that can answer from course content.
- 🤖 [Asyntai](https://asyntai.com/) ![Premium](https://img.shields.io/badge/Premium-orange) - A multilingual AI chatbot trained on course materials, installed as a plugin or a JavaScript snippet.
- 🔗 [AI Connector](https://marketplace.moodle.com/plugins/local_ai_connector) ![Free](https://img.shields.io/badge/Free-green) - Connects Moodle to ChatGPT, DALL-E, Stable Diffusion, and other AI services for use in other plugins.
- 📊 [Datacurso AI Provider](https://marketplace.moodle.com/plugins/aiprovider_datacurso) ![Free](https://img.shields.io/badge/Free-green) - An AI provider for Moodle's AI subsystem backed by Datacurso's services.
- ❓ [Generative AI Question Bank](https://marketplace.moodle.com/plugins/qbank_genai) ![Free](https://img.shields.io/badge/Free-green) - Generates quiz questions from course content such as documents and text passages.
- 🤖 [OpenAI Compatible API Provider](https://marketplace.moodle.com/plugins/aiprovider_openaicompatible) ![Free](https://img.shields.io/badge/Free-green) - Connects Moodle's AI subsystem to any service with an OpenAI-compatible API, including local models via Ollama or Groq.
- 🤖 [Gemini API Provider](https://marketplace.moodle.com/plugins/aiprovider_gemini) ![Free](https://img.shields.io/badge/Free-green) - Google Gemini for text generation, summarization, explanation, and image creation. Part of Moodle core since 5.2.
- ☁️ [Amazon Bedrock API Provider](https://marketplace.moodle.com/plugins/aiprovider_bedrock) ![Free](https://img.shields.io/badge/Free-green) - Access to foundation models on Amazon Bedrock with data kept in your AWS regions. Part of Moodle core since 5.2.
- 🎓 [Course Creator AI](https://marketplace.moodle.com/plugins/local_coursegen) ![Free](https://img.shields.io/badge/Free-green) - Generates a course structure, activities, and content from a topic description.
- 🚀 [CourseAI](https://moodle.com/news/moodle-plugin-courseai/) ![Premium](https://img.shields.io/badge/Premium-orange) - Turns a topic description or uploaded materials (PDFs, videos, audio) into a structured course with native activities. Built by three Moodle Premium Partners.
- 🤖 [SmartEdu AI Block](https://marketplace.moodle.com/plugins/block_smartedu) ![Free](https://img.shields.io/badge/Free-green) - A course block that answers students with Gemini, ChatGPT, or local Ollama models.
- ⚖️ [AI Assessment Scale](https://marketplace.moodle.com/plugins/local_assignmentnotice) ![Free](https://img.shields.io/badge/Free-green) - Labels assignments with their level on the AI Assessment Scale, so students know how they may use generative AI.
- 📝 [AI Grade](https://marketplace.moodle.com/plugins/local_aigrade) ![Free](https://img.shields.io/badge/Free-green) - Drafts grades and feedback for assignment submissions for the teacher to review.

### 📱 Mobile & Accessibility

Mobile access and accessible course content. Moodle targets WCAG 2.2 AA conformance.

- 📱 [Moodle App](https://moodle.com/products/moodle-app/) ![Free](https://img.shields.io/badge/Free-green) - The official app for iOS and Android with offline access and push notifications, accredited to WCAG 2.2 Level AA in April 2025. Since 5.2, administrators can add custom items to the app's user menu.
- ♿ [Accessibility Toolbar](https://marketplace.moodle.com/plugins/local_accessibility) ![Free](https://img.shields.io/badge/Free-green) - Lets each user adjust font size, contrast, spacing, and other display settings.
- 🗣️ [ReadSpeaker](https://www.readspeaker.com/) ![Premium](https://img.shields.io/badge/Premium-orange) - Text-to-speech that reads course content aloud.
- 🎨 [Brickfield Accessibility Toolkit](https://brickfield.ie/) ![Premium](https://img.shields.io/badge/Premium-orange) - Finds and helps fix accessibility problems in course content. A starter version is built into Moodle.
- 📖 [Ally](https://marketplace.moodle.com/plugins/tool_ally) ![Premium](https://img.shields.io/badge/Premium-orange) - Checks course files for accessibility and generates alternative formats such as audio, ePub, and tagged PDF.

### 🎮 Gamification

Game mechanics that motivate students: points, levels, badges, and quests.

- 🎲 [Game](https://marketplace.moodle.com/plugins/mod_game) ![Free](https://img.shields.io/badge/Free-green) - Hangman, crossword, cryptex, and other games built from glossaries and question banks.
- 🏆 [Level Up!](https://marketplace.moodle.com/plugins/block_xp) ![Free](https://img.shields.io/badge/Free-green) - Experience points and levels for course engagement, awarded automatically for student activity.
- 🏅 [Badges](https://docs.moodle.org/en/Badges) ![Free](https://img.shields.io/badge/Free-green) - Built-in digital badges for achievements and milestones, based on Open Badges (version 3.0 since Moodle 5.0).
- 🎯 [Stash](https://marketplace.moodle.com/plugins/block_stash) ![Free](https://img.shields.io/badge/Free-green) - Hide items across a course for students to collect and trade.
- 📈 [Leaderboard](https://marketplace.moodle.com/plugins/block_leaderboard) ![Free](https://img.shields.io/badge/Free-green) - Ranks students or groups by points earned in course activities.
- 🎯 [Ludilearn](https://marketplace.moodle.com/plugins/format_ludilearn) ![Free](https://img.shields.io/badge/Free-green) - Adaptive gamification that adjusts game elements to each learner's profile; developed through academic research.
- 🕹️ [PlayerHUD](https://marketplace.moodle.com/plugins/block_playerhud) ![Free](https://img.shields.io/badge/Free-green) - A gamification engine with XP, levels, inventory, quests, RPG characters, an NPC shop, and a leaderboard. Includes an optional AI assistant to generate items and a drop system to hide collectibles in course content.

### 💬 Communication

Discussion, messaging, and live meetings.

- 💬 [Forum](https://docs.moodle.org/en/Forum_activity) ![Free](https://img.shields.io/badge/Free-green) - The built-in discussion activity. Since 5.2, Q&A forums show responses in real time, and forums can be locked after a period of inactivity.
- 💬 [Chat](https://marketplace.moodle.com/plugins/mod_chat) ![Free](https://img.shields.io/badge/Free-green) - Real-time text chat. Removed from Moodle core in 5.0 and available as an additional plugin.
- 📝 [Journal](https://marketplace.moodle.com/plugins/mod_journal) ![Free](https://img.shields.io/badge/Free-green) - Private reflective journals that only the student and the teacher can read.
- 📧 [Quickmail](https://marketplace.moodle.com/plugins/block_quickmail) ![Free](https://img.shields.io/badge/Free-green) - Sends email to course participants, groups, or roles from a course block.
- 📹 [Zoom Meeting](https://marketplace.moodle.com/plugins/mod_zoom) ![Free](https://img.shields.io/badge/Free-green) - Schedules Zoom meetings from a course and tracks participation.
- 🎬 [STREAM Video Platform](https://marketplace.moodle.com/plugins/mod_stream) ![Premium](https://img.shields.io/badge/Premium-orange) - Video hosting and streaming inside courses, with interactive features and viewing analytics.
- 📱 [SMS Gateways](https://docs.moodle.org/en/SMS_gateways) ![Free](https://img.shields.io/badge/Free-green) - Built-in SMS notifications (since 5.0) through providers such as AWS SNS, for example for assignment deadlines.

### 📝 Assessment & Testing Enhancements

Question types, proctoring, and peer assessment beyond the standard quiz.

#### 🎯 Advanced Question Types

- ✏️ [Gapfill](https://marketplace.moodle.com/plugins/qtype_gapfill) ![Free](https://img.shields.io/badge/Free-green) - Fill-in-the-blank questions with typing, drag-and-drop, or dropdowns; supports regular expressions for answer matching.
- 🔤 [Word Select](https://marketplace.moodle.com/plugins/qtype_wordselect) ![Free](https://img.shields.io/badge/Free-green) - Students select words in a text, for grammar, proofreading, and reading comprehension.
- 🔢 [Pattern Match](https://marketplace.moodle.com/plugins/qtype_pmatch) ![Free](https://img.shields.io/badge/Free-green) - Short free-text answers graded with pattern-matching rules.
- 🧮 [STACK](https://marketplace.moodle.com/plugins/qtype_stack) ![Free](https://img.shields.io/badge/Free-green) - Mathematics and science questions evaluated by a computer algebra system, with randomized variants and detailed feedback.
- 🎲 [All-or-Nothing Multiple Choice](https://marketplace.moodle.com/plugins/qtype_multichoiceset) ![Free](https://img.shields.io/badge/Free-green) - Multiple choice where students must select every correct answer to get credit.
- 📊 [Ordering](https://marketplace.moodle.com/plugins/qtype_ordering) ![Free](https://img.shields.io/badge/Free-green) - Students drag items into the correct order, for procedures, timelines, and processes.

#### 🛡️ Proctoring & Academic Integrity

- 🔒 [Safe Exam Browser](https://marketplace.moodle.com/plugins/quizaccess_safeexambrowser) ![Free](https://img.shields.io/badge/Free-green) - Locks down the student's device during quizzes, restricting other applications and websites.
- 👁️ [Proctorio](https://proctorio.com/) ![Premium](https://img.shields.io/badge/Premium-orange) - Automated online proctoring with identity verification, browser lockdown, and flagging of suspicious behavior.
- 🧪 [Respondus LockDown Browser](https://web.respondus.com/he/lockdownbrowser/) ![Premium](https://img.shields.io/badge/Premium-orange) - A locked browser that prevents printing, copying, and switching applications until the quiz is submitted.
- 🔒 [Quilgo Proctoring](https://marketplace.moodle.com/plugins/quizaccess_quilgo) ![Premium](https://img.shields.io/badge/Premium-orange) - Quiz proctoring with webcam and screen recording and behavior analysis.
- 🛡️ [Compilatio](https://marketplace.moodle.com/plugins/plagiarism_compilatio) ![Premium](https://img.shields.io/badge/Premium-orange) - Plagiarism and AI-generated content detection for assignments, with similarity reports.
- ✏️ [Cursive](https://marketplace.moodle.com/plugins/tiny_cursive) ![Premium](https://img.shields.io/badge/Premium-orange) - Authorship verification for written work: analyzes how a text was written in the editor to help confirm a student wrote it.

#### 👥 Peer & Collaborative Assessment

- 🤝 [Workshop](https://docs.moodle.org/en/Workshop_activity) ![Free](https://img.shields.io/badge/Free-green) - The built-in peer assessment activity with assessment forms, example submissions, and automatic allocation of reviewers.
- 📋 [Peer Work](https://marketplace.moodle.com/plugins/mod_peerwork) ![Free](https://img.shields.io/badge/Free-green) - Group assignments in which students grade each other's contributions, and the group grade is adjusted per student.

[🔝 Back to top](#-contents)

## 🔗 Integrations & External Systems

Connect Moodle with cloud storage, productivity suites, and external learning tools.

### ☁️ Cloud Storage Repositories

- 📁 [Google Drive Repository](https://docs.moodle.org/en/Google_Drive_repository) ![Free](https://img.shields.io/badge/Free-green) - Built-in access to files in Google Drive when adding content to a course.
- 📂 [Nextcloud Repository](https://docs.moodle.org/en/Nextcloud_repository) ![Free](https://img.shields.io/badge/Free-green) - Built-in access to Nextcloud and ownCloud files, for institutions that keep storage on their own servers.
- 🗂️ [OneDrive for Business](https://marketplace.moodle.com/plugins/repository_office365) ![Free](https://img.shields.io/badge/Free-green) - Access to OneDrive and SharePoint files; part of the Microsoft 365 integration suite.
- 📦 [Dropbox Repository](https://docs.moodle.org/en/Dropbox_repository) ![Free](https://img.shields.io/badge/Free-green) - Built-in access to files in Dropbox.
- 🌐 [WebDAV Repository](https://docs.moodle.org/en/WebDAV_repository) ![Free](https://img.shields.io/badge/Free-green) - Built-in access to any WebDAV-compatible storage.

### 🏢 Microsoft 365 & Google Workspace

- 🟦 [Microsoft 365 Integration](https://marketplace.moodle.com/plugins/local_o365) ![Free](https://img.shields.io/badge/Free-green) - Single sign-on, OneDrive, Teams meetings, Outlook calendar sync, and SharePoint for Microsoft 365 organizations.

### 🔌 LTI (Learning Tools Interoperability)

- 🔗 [LTI 1.3 Advantage](https://docs.moodle.org/en/External_tool) ![Free](https://img.shields.io/badge/Free-green) - Built-in LTI 1.3 support as tool consumer and provider, including deep linking for choosing content from an external tool.
- 🧪 [ICTEXAM Assessment (mod_ictexam)](https://github.com/ictinnovations/moodle-mod_ictexam) ![Free](https://img.shields.io/badge/Free-green) - GPLv3 activity module that launches an ICTEXAM exam paper over LTI 1.3 inside the course page and writes the score back to the gradebook through AGS. Handles backup, restore and the recycle bin; Moodle 4.1 to 4.5. The plugin is free and open source, the exam service behind it is hosted.

[🔝 Back to top](#-contents)

## 🎨 Themes

Themes change the look and navigation of a whole site. Moodle 5.x themes are built on Bootstrap 5.

### Premium Themes

- 🎨 [Edwiser RemUI](https://edwiser.org/remui-moodle-theme/) ![Premium](https://img.shields.io/badge/Premium-orange) - A customizable theme with a modern interface, page layouts, and a visual customizer.
- 🎓 [Lumo](https://elearning.3rdwavemedia.com/moodle-themes/moodle-theme-lumo/) ![Premium](https://img.shields.io/badge/Premium-orange) - A clean Moodle 5.x theme in the style of platforms like Coursera and edX, for higher education and corporate training.
- 🏫 [Lambda](https://themeforest.net/item/lambda-premium-moodle-theme/19307139) ![Premium](https://img.shields.io/badge/Premium-orange) - A long-running ThemeForest theme with multiple layouts and many customization options.
- 🌟 [Edutor](https://elearning.3rdwavemedia.com/moodle-themes/moodle-theme-edutor/) ![Premium](https://img.shields.io/badge/Premium-orange) - A Bootstrap 5 theme with six color schemes and branding options.
- 🎓 [Edly](https://themeforest.net/item/edly-moodle-lms-education-theme/42771060) ![Premium](https://img.shields.io/badge/Premium-orange) - A Moodle 5 theme for online coaching, training centers, schools, and universities, focused on course discovery and enrolment.

### Free Themes

- 🚀 [Boost](https://docs.moodle.org/en/Themes) ![Free](https://img.shields.io/badge/Free-green) - The default core theme, built on Bootstrap 5 since Moodle 5.0.
- 📱 [Moove](https://marketplace.moodle.com/plugins/theme_moove) ![Free](https://img.shields.io/badge/Free-green) - A clean, popular theme that is maintained for Moodle 5.x.
- 🎨 [Adaptable](https://marketplace.moodle.com/plugins/theme_adaptable) ![Free](https://img.shields.io/badge/Free-green) - A highly configurable theme with control over layouts, colors, fonts, and block regions.
- 🌟 [Boost Union](https://marketplace.moodle.com/plugins/theme_boost_union) ![Free](https://img.shields.io/badge/Free-green) - Extends Boost with many configuration options for branding without custom code; used on thousands of sites.
- 🎨 [Boost Magnific](https://marketplace.moodle.com/plugins/theme_boost_magnific) ![Free](https://img.shields.io/badge/Free-green) - A Boost-based theme with richer typography, color schemes, and layout options.
- 🏢 [Degrade](https://marketplace.moodle.com/plugins/theme_degrade) ![Free](https://img.shields.io/badge/Free-green) - A clean theme focused on readability, maintained for current Moodle 5.x releases.
- 🌰 [Almondb](https://marketplace.moodle.com/plugins/theme_almondb) ![Free](https://img.shields.io/badge/Free-green) - A multi-purpose Boost-based theme with ready-made blocks and flexible page layouts.

[🔝 Back to top](#-contents)

## ⚡ Development

Tools, documentation, and practices for building plugins and themes.

- 🐳 [Moodle Docker](https://github.com/moodlehq/moodle-docker) - The official Docker setup for a local development environment with the full Moodle stack.
- ⚙️ [Moodle Development Kit (MDK)](https://moodledev.io/general/development/tools/mdk) - A command-line tool for managing development instances, running tests, and handling patches.
- 🔄 [Moodle Plugin CI](https://github.com/moodlehq/moodle-plugin-ci) - Continuous integration for plugins on GitHub Actions: code checks, PHPUnit, and Behat on every push.
- 🧪 [PHPUnit Testing](https://moodledev.io/general/development/tools/phpunit) - Writing and running unit and integration tests for Moodle code.
- 🥒 [Behat Testing](https://moodledev.io/general/development/tools/behat) - Acceptance tests that drive a real browser through Moodle features.
- 🔌 [Plugin Types](https://moodledev.io/docs/apis/plugintypes) - The official guide to every plugin type, from activities and blocks to themes and reports.
- 🎨 [Theme Development](https://moodledev.io/docs/apis/plugintypes/theme) - How to build a theme, including SCSS, templates, and layouts.
- 📏 [Coding Style](https://moodledev.io/general/development/policies/codingstyle) - The coding style that core code and well-maintained plugins follow.
- 🧩 [Plugin Skeleton Generator](https://marketplace.moodle.com/plugins/tool_pluginskel) - Generates the files of a new plugin from a recipe, so it follows current conventions from the start.
- 📁 [Directory Restructure Guide](https://moodledev.io/general/projects/directoryrestructure) - What changed with the `/public` directory introduced in Moodle 5.1, and how to update plugins and web server configuration.
- 🔗 [Routing Engine](https://moodledev.io/general/releases/5.1) - The routing engine introduced in Moodle 5.1 for cleaner URLs and request handling.
- ⚛️ [Moodle Design System](https://github.com/moodlehq/design-system) - Moodle HQ's React-based design system with UI components, guidelines, and design assets; integrated into core in 5.2.
- 📦 [Composer Installation](https://moodledev.io/general/development/tools/composer) - Installing Moodle and managing third-party libraries with Composer, supported since 5.2.
- 📊 [OpenTelemetry Integration](https://github.com/moodlehq/moodle-package-otel) - Tracing and performance monitoring with OpenTelemetry, supported since 5.2.

[🔝 Back to top](#-contents)

## 🛠️ Tools & Utilities

Command-line tools, utilities, and companion apps for administrators and developers.

- 🔧 [Moosh](https://moosh-online.com/) - A command-line shell for administering Moodle: users, courses, plugins, and backups from the terminal.
- 🎨 [Component Library](https://moodledev.io/general/development/tools/component-library) - The interactive library of Moodle UI components and their markup, for consistent plugins and themes.
- 🔍 [Health Checker](https://marketplace.moodle.com/plugins/tool_health) ![Free](https://img.shields.io/badge/Free-green) - Checks a site for common configuration problems and suggests fixes.
- 🩺 [Lifecycle](https://marketplace.moodle.com/plugins/tool_lifecycle) ![Free](https://img.shields.io/badge/Free-green) - Automates course lifecycle steps such as notifying teachers, backing up, hiding, and deleting old courses.
- 📊 [Benchmark](https://marketplace.moodle.com/plugins/report_benchmark) ![Free](https://img.shields.io/badge/Free-green) - Runs a set of server and database performance tests and compares the results with reference values.
- 🐍 [python-moodle](https://github.com/erseco/python-moodle) - A Python CLI and library for Moodle automation, including course management and content workflows through web sessions and CAS/SSO.
- 🐳 [alpine-moodle](https://github.com/erseco/alpine-moodle) - A lightweight Moodle Docker image (~100MB) built on Alpine Linux with PHP 8.3 FPM, Nginx, Redis session support, Moosh CLI, and multi-arch support. Configurable entirely through environment variables, with pre- and post-configuration hooks.
- 🌐 [Moodle Playground](https://github.com/ateeducacion/moodle-playground) - Run Moodle directly in your browser using WebAssembly (WASM), no server required. Try it at [ateeducacion.github.io/moodle-playground](https://ateeducacion.github.io/moodle-playground/).
- 🦁 [MBZoo](https://github.com/ateeducacion/mbzoo) - Inspect Moodle course backups (`.mbz`) directly in your browser without installing Moodle or uploading the backup. Explore course structure, activities, content, and files locally. Try it at [ateeducacion.github.io/mbzoo](https://ateeducacion.github.io/mbzoo/).

[🔝 Back to top](#-contents)

## ☁️ Hosting & Services

Where to run Moodle, from managed hosting to your own servers.

### Managed Hosting

- ☁️ [MoodleCloud](https://moodle.com/products/moodlecloud/) ![Premium](https://img.shields.io/badge/Premium-orange) - Moodle HQ's own hosting, with plans from small classrooms to larger organizations.
- 🚀 [ScalaHosting](https://www.scalahosting.com/moodle-hosting.html) ![Premium](https://img.shields.io/badge/Premium-orange) - Managed cloud VPS plans configured for Moodle.
- 🔧 [Moclusters](https://www.moclusters.com/) ![Premium](https://img.shields.io/badge/Premium-orange) - Scalable, high-availability hosting for large Moodle deployments.
- ☁️ [Elest.io](https://elest.io/open-source/moodle) ![Premium](https://img.shields.io/badge/Premium-orange) - Managed Moodle instances on the cloud provider of your choice.

### Self-Hosted & VPS

- ⚡ [DigitalOcean Tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-moodle-on-ubuntu-22-04) ![Free](https://img.shields.io/badge/Free-green) - Step-by-step installation of Moodle on an Ubuntu server.
- 📦 [Akamai Cloud (Linode) Guide](https://www.akamai.com/cloud/guides/install-moodle-on-ubuntu-22-04/) ![Free](https://img.shields.io/badge/Free-green) - Installing Moodle on Ubuntu with Apache, MySQL, and PHP.
- 🌐 [Google Cloud](https://cloud.google.com/solutions/moodle) ![Free](https://img.shields.io/badge/Free-green) - Options and reference material for running Moodle on Google Cloud.

[🔝 Back to top](#-contents)

## 🚚 Migration to Moodle

Moving from another LMS. Security incidents and restructuring at other vendors in 2025–2026 increased interest in open-source alternatives.

### 📋 Migration Planning & Strategy

- 📖 [Moodle Migration Guide](https://docs.moodle.org/en/Migration) ![Free](https://img.shields.io/badge/Free-green) - Official documentation on migrating site structure, users, course content, and grade history.

### 🛠️ Conversion & Import Tools

- 📦 [Common Cartridge Import](https://docs.moodle.org/en/IMS_Common_Cartridge_import_and_export) ![Free](https://img.shields.io/badge/Free-green) - Built-in import of IMS Common Cartridge packages, the export format of Canvas, Blackboard, and other LMSs.

### ⚠️ Risk Mitigation & Data Handling

- 🛡️ [GDPR and Privacy](https://docs.moodle.org/en/GDPR) ![Free](https://img.shields.io/badge/Free-green) - Moodle's privacy features for meeting GDPR, FERPA, and local privacy rules when moving user data.
- 💾 [Site Backup](https://docs.moodle.org/en/Site_backup) ![Free](https://img.shields.io/badge/Free-green) - Backing up a site before and after migration, and running old and new systems in parallel.

[🔝 Back to top](#-contents)

## 🚀 Versions & Releases

Moodle ships a major release every April and October. Long-term support (LTS) releases get three years of security fixes.

- 🚀 [Latest Release](https://download.moodle.org/releases/latest/) - Moodle 5.3 LTS, released on October 5, 2026.
- 📅 [Release Schedule & Support](https://moodledev.io/general/releases) - Release dates and support periods for every branch. The supported LTS versions are **5.3** (security fixes until October 2029) and **4.5** (until October 2027).
- 🆕 [What's New in Moodle 5.3 LTS](https://moodledev.io/general/releases/5.3) - October 2026: a visual refresh, an experimental dark mode for Boost, linear course navigation, learning outcomes linked to activities, an Anthropic Claude AI provider, and quiz due dates. Requires PHP 8.3 and upgrades from 4.4 or later.
- 🆕 [What's New in Moodle 5.2](https://moodledev.io/general/releases/5.2) - April 2026: Gemini and Amazon Bedrock AI providers in core, multiple markers for assignments, a refreshed dashboard and login page, React foundations and the Moodle Design System, Composer installation, and OpenTelemetry tracing.
- 🆕 [What's New in Moodle 5.1](https://moodledev.io/general/releases/5.1) - October 2025: the `/public` directory structure, a routing engine for cleaner URLs, the DeepSeek AI provider, a redesigned activity chooser, and a new course overview page.
- 🆕 [What's New in Moodle 5.0](https://moodledev.io/general/releases/5.0) - April 2025: the Ollama AI provider, SMS notifications, shared question banks, Bootstrap 5, and Open Badges 3.0. Chat and Survey left core.

[🔝 Back to top](#-contents)

## 📚 Tutorials & Guides

Step-by-step guides for each role.

### 👨‍🏫 For Educators

- 🚀 [Teacher Quick Guide](https://docs.moodle.org/en/Teacher_quick_guide) - The starting point for teachers new to Moodle.
- 🎬 [Teacher Training Videos](https://www.youtube.com/playlist?list=PLxcO_MFWQBDcyn9xpbmx601YSDnzgELkm) - Moodle HQ's playlist on teaching with Moodle.

### ⚙️ For Administrators

- 🚀 [Admin Quick Guide](https://docs.moodle.org/en/Admin_quick_guide) - A quick start for setting up and running a site.
- 📦 [Installation Quick Guide](https://docs.moodle.org/en/Installation_quick_guide) - Requirements, database setup, the installer, cron, and outgoing mail.
- 🛡️ [Security Guidelines](https://docs.moodle.org/en/Security) - Recommendations for securing a Moodle site.
- 📊 [Performance Recommendations](https://docs.moodle.org/en/Performance_recommendations) - Server, cache, and configuration settings for a faster site.

### 👨‍💻 For Developers

- 🚀 [Getting Started with Moodle Development](https://moodledev.io/general/development/gettingstarted) - Setting up a development environment and making a first change.
- 🔌 [Plugin Development Tutorial](https://docs.moodle.org/dev/Tutorial) - A step-by-step tutorial for writing a first plugin, on the read-only legacy developer wiki.

[🔝 Back to top](#-contents)

## 🎓 Courses & Learning

Structured learning paths and training.

### 🆓 Free Courses

- 👨‍💻 [Developer Basics Program](https://moodle.academy/course/view.php?id=64) - Moodle Academy's program on the fundamentals of Moodle development.
- 🛣️ [Developer Pathway](https://moodle.academy/course/index.php?categoryid=4) - Moodle Academy courses for developers, from the basics to advanced topics.
- 👨‍🏫 [Educator Courses](https://moodle.academy/course/index.php?categoryid=2) - Moodle Academy courses on teaching effectively with Moodle.
- ⚙️ [Administrator Training](https://moodle.academy/course/index.php?categoryid=3) - Moodle Academy courses on managing a Moodle site.

### 🏢 Partner Training

- 🤝 [Moodle Certified Service Providers](https://moodle.com/services/certified-service-providers/) - Moodle's certified partners, many of which offer training and consulting.

[🔝 Back to top](#-contents)

## 🎥 Videos & Channels

Video tutorials, conference talks, and channels.

### 📺 Official Channels

- 🎬 [Moodle on YouTube](https://www.youtube.com/moodle) - Official announcements, tutorials, and event recordings.
- 🎬 [MoodleMoot Global 2025 Playlist](https://www.youtube.com/playlist?list=PLxcO_MFWQBDfQ3JWliIIzfhiHEYx8Gxa8) - Recordings from MoodleMoot Global 2025 in Edinburgh, UK, on AI in education, course design, and the future of Moodle.

### 🎓 Educational Content

- 🚀 [Complete Beginner Tutorial](https://www.youtube.com/watch?v=uwe2c2KKvxI) - A beginner's walkthrough of Moodle.
- 🔧 [Development Setup](https://www.youtube.com/watch?v=Z-jd7oPxHIE) - Setting up a local Moodle development environment.

### 🌟 Community Channels

- 📺 [ELearning Portal](https://www.youtube.com/@elearningportal.education) - Moodle training videos for all levels.
- 🎯 [Ricoshae](https://www.youtube.com/@Ricoshae) - Tutorials on Moodle and other online course platforms.
- 🐱 [WiseCat](https://www.youtube.com/@Wise-Cat) - EdTech tutorials, including guides to recent Moodle versions.
- 📚 [LMS Daily](https://www.youtube.com/@lmsdaily) - Frequent videos on Moodle and e-learning.
- 💻 [Tech Gyan AI](https://www.youtube.com/@tech_gyans) - Moodle development and plugin tutorials.
- 🎓 [Get Interactive](https://www.youtube.com/@JohanVenterELearning) - Using H5P and Moodle for interactive teaching.
- 📹 [Moodle 2025 Tutorial Series](https://www.youtube.com/playlist?list=PLcm4ccgYk-YBlEgyqzVMeNoxnQkNCC-8S) - A 2025 playlist from login and profile setup to course creation and grading.

[🔝 Back to top](#-contents)

## 📖 Books & Publications

Books on course design and administration.

- 📚 [Moodle 4 E-Learning Course Development](https://www.packtpub.com/en-us/product/moodle-4-e-learning-course-development-9781801078399) - Creating courses in Moodle 4.x with instructional design principles.
- 🎨 [Moodle Administration Essentials](https://www.packtpub.com/en-us/product/moodle-administration-essentials-9781784393182) - Setting up, maintaining, and supporting a Moodle site.
- 📖 [Moodle Course Design Best Practices](https://www.amazon.com/Moodle-Course-Design-Best-Practices/dp/1783286814) - Instructional design principles applied to Moodle courses.
- 🔧 [Moodle Administration: An administrator's guide](https://www.amazon.com/Moodle-Administration-administrators-configuring-customizing/dp/1801816727) - Configuring, securing, and customizing Moodle for organizations of any size, with over 120 infographics.

[🔝 Back to top](#-contents)

## 👥 Community

Where Moodle users and developers meet, and how to contribute to Moodle itself.

### 💬 Forums & Support

- 🌍 [Moodle Community](https://moodle.com/community/) - Moodle HQ's overview of community forums, events, and resources.
- 🎮 [Reddit Community](https://www.reddit.com/r/moodle/) - A subreddit for Moodle questions and discussions.

### 🌐 Social Networks

- 🐦 [Moodle on X](https://x.com/moodle) - The official account for news and updates.
- 🐘 [Moodle on Mastodon](https://mastodon.online/@moodle) - Moodle on the federated social network Mastodon.

### 📰 News

- 📰 [Moodle News](https://moodle.com/news/) - Official announcements, product updates, and the monthly Edit Mode newsletter.

*MoodleNet was closed on April 24, 2026, and moodle.net now redirects to moodle.org.*

### 🤝 Contributing to Moodle

- 🐞 [Moodle Tracker](https://tracker.moodle.org/) - Report bugs and propose features for Moodle itself.
- 💻 [Development Process](https://moodledev.io/general/development/process) - How code gets into Moodle: from an issue in the tracker to integration and release.
- 🗓️ [Developer Meetings](https://moodledev.io/general/community/meetings) - Regular open meetings where Moodle HQ and community developers share progress.
- 🌐 [Translating Moodle](https://lang.moodle.org/) - Help translate Moodle into your language.

[🔝 Back to top](#-contents)

## 🌍 Conferences & Events

MoodleMoots are conferences for educators, administrators, and developers, run by Moodle HQ and its partners around the world. The [official events calendar](https://moodle.com/events/) has current dates.

- 🌐 [MIX (Moodle Ideas Exchange)](https://moodle.com/events/) - Moodle's flagship annual conference, formerly MoodleMoot Global. The 2026 edition was planned for Istanbul and is being relocated; see the events page for updates.
- 🇦🇺 [MoodleMoot Australia](https://www.catalyst-au.net/moodle-moot-event-australia) - Hosted by Catalyst IT Australia; the 2026 edition is in Melbourne on November 24.
- 🇩🇪 [MoodleMoot DACH](https://moodlemootdach.org/) - The conference for Germany, Austria, and Switzerland, with DevCamp and BarCamp formats; held at ETH Zurich in 2026.
- 🇩🇰 [MoodleMoot Nordic](https://www.moodlemootnordic.com/) - The Nordic conference, hosted by a group of Nordic Moodle partners; Copenhagen in 2026.
- 🇪🇪 [MoodleMoot Estonia](https://vextur.com/moodlemoot-estonia-2026/) - Hosted by Vextur in Tallinn.
- 🇨🇿 [MoodleMoot Czech Republic](https://moodlemoot.pragodata.cz/) - Hosted by PragoData Consulting.
- 🇮🇹 [MoodleMoot Italia](https://eventi.aium.it/event/9/) - Hosted by AIUM, the Italian Moodle users association.
- 🇧🇷 [MoodleMoot Brasil](https://brasil.moodlemoot.org/) - Hosted in São Paulo.
- 🇨🇴 [MoodleMoot Colombia](https://moodlecolombia.com/) - Hosted by Buen Data SAS in Bogotá.
- 🇵🇪 [MoodleMoot Perú](https://moodlemootperu.com/) - Hosted by Industria E in Lima.
- 🇧🇩 [MoodleMoot Bangladesh](https://brainstation-23.com/moodle-moot/) - Hosted by Brain Station 23 in Dhaka.

Other regional MoodleMoots, including Chile, Croatia, Ecuador, Costa Rica, the Philippines, El Salvador, and the Francophone Moot, are listed in the official calendar.

[🔝 Back to top](#-contents)

## 💼 Jobs & Careers

Finding work in the Moodle ecosystem.

### 🏢 Official Opportunities

- 🚀 [Moodle Careers](https://moodle.com/careers/) - Job openings at Moodle HQ, a remote-first company.
- 🤝 [Certified Service Providers](https://moodle.com/services/certified-service-providers/) - Moodle's partner network, a common employer of Moodle developers and administrators.

### 🔍 Job Boards

- 💼 [Indeed](https://www.indeed.com/q-moodle-jobs.html) - Moodle-related positions on a general job board.
- 🌐 [LinkedIn Jobs](https://www.linkedin.com/jobs/moodle-jobs) - Professional openings that mention Moodle.
- 🎓 [HigherEdJobs](https://www.higheredjobs.com/search/moodle) - Higher education roles that involve Moodle.

### 🌍 Freelance

- 💻 [Upwork](https://www.upwork.com/freelance-jobs/moodle/) - Freelance Moodle projects.
- 🎯 [Fiverr](https://www.fiverr.com/search/gigs?query=moodle) - Freelance Moodle development and administration services.

[🔝 Back to top](#-contents)

## 🌐 Multilingual Resources

Moodle is translated into more than 100 languages.

### 🌍 Language Packs

- 🌍 [Language Packs for Moodle 5.3](https://download.moodle.org/langpack/5.3/) - Official language packs. Administrators usually install them from *Site administration › General › Language › Language packs*.

### 📚 Localized Documentation

- 🇪🇸 [Documentación en Español](https://docs.moodle.org/es/) - The official documentation in Spanish.
- 🇫🇷 [Documentation Française](https://docs.moodle.org/fr/) - The official documentation in French.
- 🇩🇪 [Deutsche Dokumentation](https://docs.moodle.org/de/) - The official documentation in German.

### 🔧 Multilingual Tools

- 🌐 [Multi-Language Content (v2)](https://marketplace.moodle.com/plugins/filter_multilang2) ![Free](https://img.shields.io/badge/Free-green) - Shows each user the version of a text in their language, for multilingual courses.

[🔝 Back to top](#-contents)

## 📢 News & Ecosystem Updates (2025–2026)

The most significant milestones and changes in the Moodle ecosystem in 2025–2026.

### 🎉 Milestones

- 📈 **500 Million Users** - In December 2025, Moodle announced more than 500 million users on registered sites, across over 148,000 installations in 234 countries, 23 years after the first release.
- 🏆 **GSV 150** - Moodle was named to the 2026 GSV 150, a list of the most transformational companies in digital learning and workforce skills, selected from over 3,000 companies.
- 🌍 **B Corp Recertification** - Moodle was recertified as a B Corporation in July 2025, with certification extended to the US and India.

### 🚀 Product & Platform News

- 🚀 **Moodle 5.3 LTS** - Released on October 5, 2026; security fixes until October 2029.
- 🛒 **Moodle Marketplace** - Launched in mid-2026 to replace the plugins directory, which became read-only on July 14, 2026. It lists free and paid plugins, with payments through Stripe, invoicing, and quality checks; old plugin directory links redirect to it.
- 🔒 **MFA on Community Sites** - In February 2026, Moodle enabled multi-factor authentication on its community sites, including moodle.org.
- 📴 **MoodleNet Closure** - MoodleNet, Moodle's federated network for sharing educational resources, closed on April 24, 2026; moodle.net now redirects to moodle.org.
- 🌐 **MIX (Moodle Ideas Exchange)** - MoodleMoot Global was rebranded as MIX in 2025. The 2026 edition was planned for Istanbul and is being relocated.
- 🤖 **CourseAI** - Three Moodle Premium Partners (E-learning Touch', 3ipunt, and Moxis) built CourseAI, which generates structured courses from a topic description or uploaded materials.
- 🔗 **Moodle Certified Integrations** - In June 2026, Moodle expanded its Certified Integrations program for third-party tools reviewed by Moodle HQ for quality and security.

### 📊 LMS Market Context

- The global LMS market is estimated at USD 31.6–37.1 billion in 2026, growing 16–20% a year, and is projected to exceed USD 100 billion by 2032.
- A major **Canvas security breach** in May 2026 (about 275 million records across 8,809 institutions) increased interest in open-source and self-hosted LMS alternatives.
- **Blackboard/Anthology** filed for Chapter 11 bankruptcy in September 2025 and emerged as a standalone Blackboard in February 2026.

[🔝 Back to top](#-contents)

## 🤝 Contributing

Contributions are welcome, including from plugin authors and vendors who disclose their affiliation.

- **Add a resource:** fill in the [submission form](https://github.com/moosensei/awesome-moodle/issues/new?template=add-resource.yml). A bot checks the account, link, and wording and opens a pull request. A maintainer reviews every pull request; nothing is merged automatically.
- **Report a broken link or an outdated entry:** use the [change report form](https://github.com/moosensei/awesome-moodle/issues/new?template=update-resource.yml).
- **Report phishing, malware, or a hijacked link:** privately, as described in [SECURITY.md](SECURITY.md).

Read [CONTRIBUTING.md](CONTRIBUTING.md) for what we list, the rules for vendors, and how review works. Questions: [madewithmoodle@gmail.com](mailto:madewithmoodle@gmail.com).

## 📜 License

[![CC0](https://licensebuttons.net/p/zero/1.0/88x31.png)](https://creativecommons.org/publicdomain/zero/1.0/)

This list is dedicated to the public domain under [CC0 1.0 Universal](LICENSE): use, modify, and share it for any purpose, without asking.

[🔝 Back to top](#-contents)
