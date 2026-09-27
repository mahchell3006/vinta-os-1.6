# Graph Report - vinta-os-app-essembled-main  (2026-09-27)

## Corpus Check
- 256 files · ~212,981 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 13 file(s) not represented in the graph (top: (none) 5, .ini 2, .db 1)

## Summary
- 2519 nodes · 6333 edges · 117 communities (80 shown, 37 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 378 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0287abcf`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- extensions.py
- routes/students.py
- SettingsPage.tsx
- MultiPaymentError
- Session
- schemas/students.py
- schemas/attendance.py
- schemas/billing.py
- User
- ClassCardMenu.tsx
- tenant_required
- vinta-school-os/package.json
- billing.ts
- WeekView.tsx
- owner_only
- Student
- SessionWindowModal.tsx
- react
- format_dzd
- AcademySettings
- Session
- SchedulingModal.tsx
- BillingConfig.tsx
- jwt_required
- routes/settings.py
- routes/calendar.py
- TeacherHoursLog
- SessionCheckInModal.tsx
- routes/auth.py
- schemas/notifications.py
- env.py
- schemas/teachers.py
- TestCheckOutFlow
- TestSessionCRUD
- compilerOptions
- test_cron_jobs.py
- Academy Root Entity
- constants.ts
- jwt_required
- routes/teachers.py
- routes/classes.py
- DashboardPage.tsx
- toast
- SessionDetail.tsx
- StudentDrawer.tsx
- Luxury School OS Concept
- formatters.ts
- PaymentHistoryList.tsx
- log_activity
- ClassesPage.tsx
- ActivityLog.tsx
- student.ts
- router.tsx
- cn
- compilerOptions
- TestBillingStatusDerivation
- class.ts
- add_lifecycle_columns.py
- SessionMenu.tsx
- check_overdue_billings
- providers.tsx
- uiStore.ts
- StudentAttendanceCalendar.tsx
- create_app
- TestCheckInFlow
- test_cancel_session.py
- calendar.ts
- billing_service.py
- SessionBlock.tsx
- TestHourlyPayroll
- format_phone
- schemas/calendar.py
- parse_dzd
- Class
- validate_phone
- week_date_range
- rawval
- Avatar.tsx
- snapshot
- C-01 Hardcoded Fallback JWT Secret Vulnerability
- .oxlintrc.json
- TeacherDrawer.tsx
- ErrorBoundary
- BillingSummaryCard.tsx
- get_activity_logs
- tsconfig.json
- routes/__init__.py
- schemas/__init__.py
- tasks/__init__.py
- utils/__init__.py
- tests/__init__.py
- integration/__init__.py
- unit/__init__.py
- Graphify Knowledge Graph Rules
- deps/package.json
- Analytics & Reports Blueprint (/api/analytics)
- Settings Blueprint (/api/settings)
- Teacher Revenue Split Model
- C-02 SocketIO Wildcard CORS Vulnerability
- C-05 Missing Token Revocation Mechanism
- C-06 Unauthenticated Owner Creation Risk
- T3 Hamburger Menu Instance Overrides
- T4 Auto-Link Guest Swap Mechanism
- T6 Free Session Payout Zero Logic
- T7 Void & Compensate Cancellation Freeze
- T8 Scheduling Window (Weekly vs Temporary)
- Vinta School OS App Icon
- Vite Tooling Asset
- conftest.py
- routes/notifications.py
- themeStore.ts
- marshmallow
- Test Verification Fixture (acad.txt)
- Test Verification Fixture (academy_id.txt)
- Test Verification Fixture (class_id.txt)
- Test Verification Fixture (student_id.txt)
- Test Verification Fixture (tok.txt)

## God Nodes (most connected - your core abstractions)
1. `cn()` - 180 edges
2. `tenant_required()` - 112 edges
3. `react` - 81 edges
4. `Session` - 69 edges
5. `lucide-react` - 69 edges
6. `User` - 57 edges
7. `Class` - 53 edges
8. `Student` - 47 edges
9. `api` - 42 edges
10. `useAuthStore` - 41 edges

## Surprising Connections (you probably didn't know these)
- `dbval()` --uses--> `AcademySettings`  [INFERRED]
  .tmp-relprobe/probe_billing_rules.py → Backend/vinta-academy-backend/app/models/academy.py
- `Login Screen Hero Artwork` --conceptually_related_to--> `Glassmorphic Design Tokens (--gold / --emerald)`  [INFERRED]
  vinta-school-os/src/assets/hero.png → Docs/Notes.md
- `make_session()` --uses--> `Session`  [INFERRED]
  .tmp-relprobe/probe_audit_fk.py → Backend/vinta-academy-backend/app/models/scheduling.py
- `credits_of()` --uses--> `StudentSubscription`  [INFERRED]
  .tmp-relprobe/probe_finalise.py → Backend/vinta-academy-backend/app/models/billing.py
- `make_session()` --uses--> `Session`  [INFERRED]
  .tmp-relprobe/probe_finalise.py → Backend/vinta-academy-backend/app/models/scheduling.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Multi-Tenant Core Architecture & Domain Boundaries** — docs_documentation_tenant_isolation_model, docs_documentation_entity_academy, backend_api_architecture_overview, docs_documentation_billing_architecture [EXTRACTED 1.00]
- **Session Lifecycle & Attendance Grid Flow** — docs_documentation_entity_scheduled_session, docs_documentation_attendance_workflow, vinta_tasks_t1_session_lifecycle_lock, vinta_tasks_t2_false_until_true_attendance [INFERRED 0.85]

## Communities (117 total, 37 thin omitted)

### Community 0 - "extensions.py"
Cohesion: 0.04
Nodes (86): Vinta School OS — Extension Initialization Centralized extension instances for…, Vinta School OS — Application Factory Creates and configures the Flask…, Vinta School OS — Academy & Tenant Models Academy (tenant root),…, Vinta School OS — Attendance Model SessionStudent: tracks check-in/out per…, Vinta School OS — Activity Log & Audit Trail Model Every significant action is…, PaymentLog, Vinta School OS — Billing Models PaymentPlan, StudentBilling, PaymentLog…, One record per billing cycle per student. Core billing entity. (+78 more)

### Community 1 - "routes/students.py"
Cohesion: 0.15
Nodes (23): add_guardian(), bulk_enroll_students(), create_student(), delete_student(), enroll_student(), get_stats(), get_student(), list_guardians() (+15 more)

### Community 2 - "SettingsPage.tsx"
Cohesion: 0.08
Nodes (28): AcademyProfile(), AcademyProfileProps, TERM_OPTIONS, WORKING_DAYS, AddStaffModal(), AddStaffModalProps, inputCls, Appearance() (+20 more)

### Community 3 - "MultiPaymentError"
Cohesion: 0.50
Nodes (3): MultiPaymentError, Exception, A multi-payment could not be recorded — nothing was charged. Raised instead of…

### Community 4 - "Session"
Cohesion: 0.04
Nodes (90): Many-to-many: Session ↔ Student. Tracks attendance (is_present, check-in/out…, SessionStudent, ActivityLog, Audit trail. Every significant action in the system is logged with user_id —…, A concrete class session on a specific date. Generated from Schedule or created…, Session, absence_consumes_credit(), count_gap_sessions() (+82 more)

### Community 5 - "schemas/students.py"
Cohesion: 0.11
Nodes (25): AddGuardianRequestSchema, CreateStudentRequestSchema, CreateStudentResponseSchema, EnrollmentSchema, EnrollResponseSchema, EnrollStudentRequestSchema, GuardianSchema, Schema (+17 more)

### Community 6 - "schemas/attendance.py"
Cohesion: 0.10
Nodes (27): AddToSessionRequestSchema, AddToSessionResponseSchema, AutoCheckoutRequestSchema, AutoCheckoutResponseSchema, CheckInRequestSchema, CheckInResponseSchema, CheckOutRequestSchema, CheckOutResponseSchema (+19 more)

### Community 7 - "schemas/billing.py"
Cohesion: 0.06
Nodes (51): AgingBucketsResponseSchema, BillingStatsResponseSchema, CreatePlanRequestSchema, FinalizeSessionRequestSchema, FinalizeSessionResponseSchema, MarkPayoutPaidRequestSchema, PaymentPlanListResponseSchema, PaymentPlanSchema (+43 more)

### Community 8 - "User"
Cohesion: 0.06
Nodes (33): Every person who logs into the system. Owner or Staff., Hash a 4-digit PIN using bcrypt., Verify a PIN against the stored hash., Hash a password using bcrypt., Verify a password against the stored hash., Set a new password hash (owner only)., User, create_owner() (+25 more)

### Community 9 - "ClassCardMenu.tsx"
Cohesion: 0.16
Nodes (17): ClassCardMenu(), EndClassModal(), FreeChip(), isRunning(), NoSessionTrigger(), RunningLight(), RunningLightState, serverMessage() (+9 more)

### Community 10 - "tenant_required"
Cohesion: 0.11
Nodes (41): check_overdue(), create_plan(), finalize_session(), get_aging_buckets(), get_revenue(), get_revenue_chart(), get_stats(), list_payouts() (+33 more)

### Community 11 - "vinta-school-os/package.json"
Cohesion: 0.04
Nodes (44): axios, clsx, oxlint, ref_path, recharts, tailwind-merge, tailwindcss, @tailwindcss/vite (+36 more)

### Community 12 - "billing.ts"
Cohesion: 0.09
Nodes (23): PaymentHistoryListProps, UseStudentBillingResult, AgingBucket, BillingRingData, BillingState, BillingStats, CreatePaymentPlanRequest, GroupCharge (+15 more)

### Community 13 - "WeekView.tsx"
Cohesion: 0.19
Nodes (26): DayView(), decimalToTime(), snapHour(), toCalendarSession(), yToTime(), decimalToTime(), snapHour(), toCalendarSession() (+18 more)

### Community 14 - "owner_only"
Cohesion: 0.07
Nodes (44): add_staff(), _coerce_bool(), deactivate_staff(), delete_staff(), export_data(), get_academy(), get_activity_log(), get_appearance() (+36 more)

### Community 15 - "Student"
Cohesion: 0.05
Nodes (56): Enrollment, Many-to-many: Student ↔ Class through Enrollment., A child enrolled in the academy., Student, create_multi_payment(), Create new billing records for students whose cycles have ended. Returns count…, Multi-teacher payment flow: one receipt covering several groups. Creates…, Multi-teacher payment: create separate subscriptions per group. Thin wrapper… (+48 more)

### Community 16 - "SessionWindowModal.tsx"
Cohesion: 0.13
Nodes (23): Select, SelectAction, SelectOption, SelectProps, inputCls, SessionWindowModalProps, buildClassPayload(), CLASS_COLOR_PRESETS (+15 more)

### Community 17 - "react"
Cohesion: 0.06
Nodes (63): lucide-react, react, Badge, BadgeProps, SemanticVariant, sizeStyles, variantAliases, variantStyles (+55 more)

### Community 19 - "AcademySettings"
Cohesion: 0.06
Nodes (33): Academy, AcademySettings, Academy SaaS subscription tier., Top-level tenant entity. One academy = one private school/academy., Per-academy configuration singleton., Subscription, create_academy(), get_academy_profiles() (+25 more)

### Community 20 - "Session"
Cohesion: 0.12
Nodes (30): DayViewProps, FinalizeSessionModalProps, SchedulingModalProps, SessionCheckInModalProps, AgendaBoardProps, PositionedSession, SessionActions(), SessionActionsProps (+22 more)

### Community 21 - "SchedulingModal.tsx"
Cohesion: 0.10
Nodes (36): errMsg(), GroupOption, inputCls, Mode, primaryBtnCls, RoomOption, SchedulingModal(), TeacherOption (+28 more)

### Community 22 - "BillingConfig.tsx"
Cohesion: 0.10
Nodes (28): Input, InputProps, BillingPage(), FinancesModal(), LogModal(), BillingConfig(), BillingConfigProps, BillingPreset (+20 more)

### Community 23 - "jwt_required"
Cohesion: 0.12
Nodes (22): add_student_to_session(), cancel_session(), create_session(), _duration_label(), get_day(), get_session_roster(), get_week(), list_sessions() (+14 more)

### Community 24 - "routes/settings.py"
Cohesion: 0.06
Nodes (49): Vinta School OS — Settings Blueprint /api/settings — Academy Config, Staff…, AcademyResponseSchema, AddStaffRequestSchema, AddStaffResponseSchema, AppearanceResponseSchema, AutomationsResponseSchema, BillingConfigResponseSchema, ProfileResponseSchema (+41 more)

### Community 25 - "routes/calendar.py"
Cohesion: 0.06
Nodes (47): export_data(), get_dashboard(), jwt_required, route, Vinta School OS — Analytics Blueprint /api/analytics — Dashboard stats, Revenue…, Export data as CSV. Supported datasets: students, billing, teacher_hours,…, Dashboard overview stats. Returns: total students, total teachers, total…, Time-series revenue data. Query params: months (default 6) (+39 more)

### Community 26 - "TeacherHoursLog"
Cohesion: 0.22
Nodes (8): Records when a teacher's hours are logged (per session)., TeacherHoursLog, export_chart_data(), export_teacher_hours(), Generate CSV for chart data based on chart type. Supports: income, enrollments,…, Generate CSV for teacher hours. Columns: Teacher, Session, Date, Hours, Subject, log_teacher_hours(), Log hours for a teacher's session.

### Community 27 - "SessionCheckInModal.tsx"
Cohesion: 0.09
Nodes (43): RosterEntry, SessionCheckInModal(), STATUS_CONFIG, StudentSearchResult, fetchBilling(), DangerConfirmModal(), VoidModal(), BILLING_RULE_DEFAULTS (+35 more)

### Community 28 - "routes/auth.py"
Cohesion: 0.07
Nodes (55): arguments, change_pin(), create_profile(), get_current_user(), get_profiles(), login(), logout(), jwt_required (+47 more)

### Community 29 - "schemas/notifications.py"
Cohesion: 0.23
Nodes (11): CreateNotificationRequestSchema, CreateNotificationResponseSchema, NotificationListResponseSchema, NotificationSchema, Schema, Notification schemas — Toast alerts, Broadcasts., POST /api/notifications, GET /api/notifications response. (+3 more)

### Community 30 - "env.py"
Cohesion: 0.09
Nodes (20): alembic, apscheduler_schedulers_background, init_scheduler(), Vinta School OS — APScheduler Setup Initializes and manages the background task…, Initialize APScheduler with all configured cron jobs. Called during application…, Gracefully shut down the scheduler., shutdown_scheduler(), get_engine() (+12 more)

### Community 31 - "schemas/teachers.py"
Cohesion: 0.14
Nodes (19): CreateTeacherRequestSchema, CreateTeacherResponseSchema, PayrollSummarySchema, Schema, Teacher schemas — CRUD, Contracts, Payroll., POST /api/teachers response., PUT /api/teachers/<id>, Single teacher in list. (+11 more)

### Community 32 - "TestCheckOutFlow"
Cohesion: 0.10
Nodes (14): integration, Test session roster operations., New session should have empty roster., Should be able to add a student to a session roster., Adding the same student twice should return existing record., Test auto-checkout trigger., Auto-checkout should check out all present students., Test student check-out from session. (+6 more)

### Community 33 - "TestSessionCRUD"
Cohesion: 0.07
Nodes (17): integration, Should update session date via PATCH., Moved session times should snap to 5-minute grid., Should cancel a session via DELETE., Test recurring schedule → session generation., Test session create/read/update/delete via API., Creating a schedule should auto-generate sessions for 12 weeks., Should create a new session with valid data. (+9 more)

### Community 34 - "compilerOptions"
Cohesion: 0.07
Nodes (26): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, baseUrl, erasableSyntaxOnly, forceConsistentCasingInFileNames, ignoreDeprecations, isolatedModules (+18 more)

### Community 35 - "test_cron_jobs.py"
Cohesion: 0.19
Nodes (17): auto_checkout_expired_sessions(), Check all in-progress sessions whose end_time has passed and auto check-out any…, _make_session(), Vinta School OS — the end-of-class cron sweep. Regression cover for two bugs…, A class that has not ended yet is left alone., A ``scheduled`` class that nobody started is the desk's to cancel. The old…, A finished class is not re-processed., A session on a given day, in a given lifecycle state. (+9 more)

### Community 36 - "Academy Root Entity"
Cohesion: 0.09
Nodes (25): Attendance Blueprint (/api/attendance), Billing & Subscriptions Blueprint (/api/billing), Calendar & Sessions Blueprint (/api/sessions), Classes & Groups Blueprint (/api/classes), Students Blueprint (/api/students), Teachers Blueprint (/api/teachers), Session Attendance & Check-in/out Flow, Student Tuition & Credit/Time Billing Architecture (+17 more)

### Community 37 - "constants.ts"
Cohesion: 0.08
Nodes (25): ACADEMY_ID_KEY, ACTIVITY_TYPES, API_BASE_URL, AvatarPreset, BREAKPOINTS, CHART_COLORS, DEFAULT_SESSION_DURATION, ENTITY_FILTER_PAGES (+17 more)

### Community 38 - "jwt_required"
Cohesion: 0.08
Nodes (38): create_classroom(), create_subject(), delete_class(), delete_classroom(), delete_schedule(), delete_subject(), get_class(), _group_payload() (+30 more)

### Community 39 - "routes/teachers.py"
Cohesion: 0.09
Nodes (35): Extensible palette entity for calendar subject colors., Subject, Junction table for teacher-subject many-to-many relationship., An instructor employed by the academy., Teacher, TeacherSubject, _clean_email(), _clean_status() (+27 more)

### Community 40 - "routes/classes.py"
Cohesion: 0.13
Nodes (25): Vinta School OS — Classes Blueprint /api/classes, /api/classrooms — Class &…, ClassListResponseSchema, ClassListSchema, ClassroomListResponseSchema, ClassroomSchema, CreateClassRequestSchema, CreateClassResponseSchema, CreateClassroomRequestSchema (+17 more)

### Community 41 - "DashboardPage.tsx"
Cohesion: 0.10
Nodes (34): CalendarPage(), hourLabel(), errMsg(), GroupOption, RoomOption, SessionWindowModal(), TeacherOption, calendarRequest() (+26 more)

### Community 42 - "toast"
Cohesion: 0.14
Nodes (12): StudentsPage, AddStudentModal(), AddStudentModalProps, ClassOption, inputClass, activePillClass(), FilterKey, StatCard() (+4 more)

### Community 43 - "SessionDetail.tsx"
Cohesion: 0.14
Nodes (17): PinStep(), PinStepProps, InfoChipProps, RosterStudent, SessionDetail, STATUS_BADGE_CLASSES, StudentRow(), StudentRowProps (+9 more)

### Community 44 - "StudentDrawer.tsx"
Cohesion: 0.21
Nodes (11): MultiPayModalProps, BillingSummaryCardProps, useStudentBilling(), useStudentProfile(), UseStudentProfileResult, ENROLLMENT_LABELS, Field(), StudentDrawer() (+3 more)

### Community 45 - "Luxury School OS Concept"
Cohesion: 0.11
Nodes (19): Flask REST API Architecture, Auth Blueprint (/api/auth), Two-Stage Auth & Profile PIN Verification Flow, Docker Compose Local Environment, Flask & SQLAlchemy Dependencies, PIN-Attributed Activity Log & Audit Trail, Algerian Private Academy Target Market, Glassmorphic Design Tokens (--gold / --emerald) (+11 more)

### Community 46 - "formatters.ts"
Cohesion: 0.18
Nodes (8): ProfileCreator(), STATUS_LABELS, statusLabel(), StudentTable(), StudentTableProps, formatPhone(), getInitials(), StudentStatus

### Community 47 - "PaymentHistoryList.tsx"
Cohesion: 0.38
Nodes (9): formatDateRange(), formatDisplayDate(), humaniseStatus(), METHOD_LABELS, methodLabel(), parseTimestamp(), PaymentHistoryList(), purchaseShape() (+1 more)

### Community 48 - "log_activity"
Cohesion: 0.22
Nodes (10): _apply_group_fields(), create_class(), _normalize_billing_model(), Create a new class. Body: { name, subject?, color?, teacher_id?, capacity?,…, Update class fields (legacy + CourseGroup money-model fields)., Map friendly billing-model names to the DB enum values., Apply any CourseGroup fields present in data. Returns applied names., update_class() (+2 more)

### Community 49 - "ClassesPage.tsx"
Cohesion: 0.06
Nodes (49): DayPicker(), DayPickerProps, sizeStyles, todayISO(), toISO(), WEEKDAYS, PinConfirmDialog(), PinConfirmDialogProps (+41 more)

### Community 50 - "ActivityLog.tsx"
Cohesion: 0.18
Nodes (10): ActivityLog, ActivityLogEntry, ActivityLogProps, ActivityRow(), ActivityRowProps, ICON_MAP, ICON_STYLE, relativeTime() (+2 more)

### Community 51 - "student.ts"
Cohesion: 0.14
Nodes (17): EmptyLine(), ProfileCard(), ProfileCardProps, StudentClasses(), StudentClassesProps, GuardianRow, safePhone(), StudentGuardians() (+9 more)

### Community 52 - "router.tsx"
Cohesion: 0.06
Nodes (43): react-router-dom, AppShell(), AuthGuard(), AuthScreen, BillingPage, CalendarPage, ClassesPage, DashboardPage (+35 more)

### Community 53 - "cn"
Cohesion: 0.09
Nodes (25): react-dom, PageContainer(), PageContainerProps, CardFooter, ConfirmDialog, ConfirmDialogProps, Drawer, DrawerProps (+17 more)

### Community 54 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 55 - "TestBillingStatusDerivation"
Cohesion: 0.06
Nodes (20): unit, Should return 0 for future due dates., Should return 0 when due date is today., Test payment plan creation and properties., Payment plans should store correct values., Term plans should have 90-day duration., Test billing status derivation logic., Status should be 'paid' when paid_date is set and paid_amount >= amount_da. (+12 more)

### Community 56 - "class.ts"
Cohesion: 0.12
Nodes (15): AttendanceStatus, CheckInRequest, ClassBillingInfo, Classroom, ClassState, ClassStats, CreateClassRequest, CreateClassroomRequest (+7 more)

### Community 57 - "add_lifecycle_columns.py"
Cohesion: 0.16
Nodes (11): main(), Additive migration — billing relations, session lifecycle, billing toggles.…, Resolve the SQLite file the app actually opens, from DATABASE_URL., resolve_db_path(), One-shot database fix — adds any missing columns to existing tables. Run once:…, main(), Schema step — activity_logs.user_id becomes nullable. WHY The audit trail has…, Resolve the SQLite file the app actually opens, from DATABASE_URL. (+3 more)

### Community 58 - "SessionMenu.tsx"
Cohesion: 0.15
Nodes (17): dangerBtnCls, FreeNextModal(), inputCls, LogEntry, MenuItem(), ModalKind, ModalShell(), PayoutRow (+9 more)

### Community 59 - "check_overdue_billings"
Cohesion: 0.50
Nodes (4): check_overdue_billings(), Check for billings that are past due_date and mark them as overdue. Returns…, check_overdue_payments(), Check all academies for billings past their due_date. Marks them as 'overdue'…

### Community 60 - "providers.tsx"
Cohesion: 0.13
Nodes (12): App(), Providers(), ProvidersProps, TOAST_COLORS, TOAST_ICONS, ToastContainer(), AppRouter(), Toast (+4 more)

### Community 61 - "uiStore.ts"
Cohesion: 0.09
Nodes (26): AppShell(), classMatches(), classRow(), GlobalSearch(), Row, ROW_STYLE, SECTION_ORDER, STUDENT_STATUS_LABEL (+18 more)

### Community 62 - "StudentAttendanceCalendar.tsx"
Cohesion: 0.23
Nodes (11): dominantState(), formatTime(), monthCells(), STATE_PRIORITY, STATE_STYLES, StateStyle, StudentAttendanceCalendar(), StudentAttendanceCalendarProps (+3 more)

### Community 63 - "create_app"
Cohesion: 0.05
Nodes (29): BaseConfig, DevelopmentConfig, ProductionConfig, Vinta School OS — Configuration Environments Dev, Test, and Production…, Shared configuration across all environments., Development environment configuration., Test environment configuration., Production environment configuration. (+21 more)

### Community 64 - "TestCheckInFlow"
Cohesion: 0.33
Nodes (4): Test student check-in to session., Staff should be able to check in a student to a session., Check-in should create an activity log entry., TestCheckInFlow

### Community 65 - "test_cancel_session.py"
Cohesion: 0.16
Nodes (21): cancel_session(), Cancel a session, recording *why*. The reason is not decoration:…, Vinta School OS — cancelling a session. ``cancel_session`` is reached from…, CANCEL_REASONS is a plain Python tuple; the column is a native enum that knows…, An unrecognised reason is a label problem, not a reason to lose the cancel., A bare DELETE still cancels; it just does not claim to know why., Tenant scoping — the lookup is by id AND academy., A class that has not run can be called off; a class that is running can be… (+13 more)

### Community 66 - "calendar.ts"
Cohesion: 0.14
Nodes (14): AddSubjectModal(), AddSubjectModalProps, COLOR_PRESETS, SubjectPalette(), SubjectPaletteProps, WeekViewProps, CalendarState, CalendarViewMode (+6 more)

### Community 67 - "billing_service.py"
Cohesion: 0.04
Nodes (72): PaymentPlan, PayoutRecord, Student purchase of a Class offer (credit-based or time-based). Table name is…, Reusable billing plans that can be assigned to students., Immutable revenue fact per conducted session allocation (DZD integers)., Teacher payout computed from gross revenue per conducted session., RevenueEntry, StudentSubscription (+64 more)

### Community 68 - "SessionBlock.tsx"
Cohesion: 0.53
Nodes (5): hexToRgba(), SessionBlock(), SessionBlockProps, formatTime(), CalendarSession

### Community 69 - "TestHourlyPayroll"
Cohesion: 0.12
Nodes (12): unit, Settling a payroll should set paid_date and status., Test hourly contract payroll calculations., Hourly payroll = total_hours × hourly_rate., Payroll with zero hours should return 0 amount., Test per-student contract payroll calculations., Per-student payroll = active_students × per_student_rate., Test payroll status transitions. (+4 more)

### Community 71 - "schemas/calendar.py"
Cohesion: 0.17
Nodes (15): CreateSessionRequestSchema, CreateSessionResponseSchema, DaySessionsResponseSchema, Schema, Calendar schemas — Session CRUD, Week/Day views, Drag-and-drop., PATCH /api/sessions/<id>, Single session in calendar view., GET /api/calendar/week response. (+7 more)

### Community 73 - "Class"
Cohesion: 0.09
Nodes (32): Class, A subject offering (e.g., 'Math — CM2'). Enrollment target for students., Recurring weekly slot defining when a class meets., Schedule, create_schedule(), Add a schedule block to a class. Body: { day_of_week, start_time, end_time,…, create_session(), generate_sessions_from_schedule() (+24 more)

### Community 77 - "Avatar.tsx"
Cohesion: 0.33
Nodes (8): Avatar, AvatarProps, getGradientForName(), getInitials(), gradientPairs, hashCode(), sizeConfig, squircleRadius()

### Community 83 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 84 - "TeacherDrawer.tsx"
Cohesion: 0.06
Nodes (44): RFC-5322, TeachersPage, ClassBillingStat(), AddTeacherModal(), AddTeacherModalProps, COMMISSION_PLACEHOLDER, COMMISSION_SUFFIX, COMMISSION_TYPES (+36 more)

### Community 86 - "BillingSummaryCard.tsx"
Cohesion: 0.21
Nodes (17): BillingCalendarCard(), BillingCalendarCardProps, CYCLE_STATUS_LABELS, statusDot(), BillingSummaryCard(), DASH, knownText(), parseISODate() (+9 more)

### Community 87 - "get_activity_logs"
Cohesion: 0.50
Nodes (4): get_activity_logs(), _map_log_type(), Get activity logs for an academy, newest first. UI shows last 30 entries with…, Map entity_type + action to UI log type for icon/color styling: - payment →…

### Community 118 - "conftest.py"
Cohesion: 0.10
Nodes (26): Classroom, A physical room in the academy., Guardian, Student guardian / emergency contact. One student can have multiple guardians., app(), auth_headers_owner(), auth_headers_staff(), classroom() (+18 more)

### Community 119 - "routes/notifications.py"
Cohesion: 0.21
Nodes (15): Notification, In-app toast notification / alert., create_notification(), get_unread_count(), list_notifications(), mark_all_read(), mark_read(), jwt_required (+7 more)

### Community 121 - "themeStore.ts"
Cohesion: 0.17
Nodes (17): FONT_SIZE_KEY, LANGUAGE_KEY, THEME_KEY, applyFontSize(), applyLanguage(), applyTheme(), FontSize, Language (+9 more)

### Community 124 - "marshmallow"
Cohesion: 0.29
Nodes (7): DashboardResponseSchema, Schema, Analytics schemas — Dashboard stats, Revenue chart, CSV export., GET /api/analytics/revenue-chart response., GET /api/analytics/dashboard response., RevenueChartResponseSchema, marshmallow

## Knowledge Gaps
- **384 isolated node(s):** `type`, `Meta`, `$schema`, `plugins`, `react/rules-of-hooks` (+379 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1135 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **37 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `tenant_required()` connect `tenant_required` to `routes/students.py`, `billing_service.py`, `jwt_required`, `routes/teachers.py`, `routes/classes.py`, `Class`, `User`, `owner_only`, `log_activity`, `AcademySettings`, `routes/notifications.py`, `jwt_required`, `routes/settings.py`, `routes/calendar.py`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Why does `Session` connect `Session` to `extensions.py`, `test_cancel_session.py`, `TestSessionCRUD`, `billing_service.py`, `test_cron_jobs.py`, `jwt_required`, `routes/teachers.py`, `routes/classes.py`, `Class`, `owner_only`, `Student`, `conftest.py`, `jwt_required`, `routes/settings.py`, `routes/calendar.py`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Why does `cn()` connect `cn` to `SettingsPage.tsx`, `ClassCardMenu.tsx`, `WeekView.tsx`, `SessionWindowModal.tsx`, `react`, `Session`, `SchedulingModal.tsx`, `BillingConfig.tsx`, `SessionCheckInModal.tsx`, `DashboardPage.tsx`, `toast`, `SessionDetail.tsx`, `StudentDrawer.tsx`, `formatters.ts`, `PaymentHistoryList.tsx`, `ClassesPage.tsx`, `ActivityLog.tsx`, `student.ts`, `router.tsx`, `SessionMenu.tsx`, `providers.tsx`, `uiStore.ts`, `StudentAttendanceCalendar.tsx`, `calendar.ts`, `SessionBlock.tsx`, `Avatar.tsx`, `TeacherDrawer.tsx`, `BillingSummaryCard.tsx`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `tenant_required()` (e.g. with `Academy` and `User`) actually correct?**
  _`tenant_required()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 40 inferred relationships involving `Session` (e.g. with `get_dashboard()` and `get_roster()`) actually correct?**
  _`Session` has 40 INFERRED edges - model-reasoned connections that need verification._
- **What connects `type`, `Meta`, `$schema` to the rest of the system?**
  _384 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `extensions.py` be split into smaller, more focused modules?**
  _Cohesion score 0.04245439469320066 - nodes in this community are weakly interconnected._