# Graph Report - vinta-os-app-essembled-main  (2026-09-27)

## Corpus Check
- 255 files · ~212,210 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 13 file(s) not represented in the graph (top: (none) 5, .ini 2, .db 1)

## Summary
- 2517 nodes · 6321 edges · 118 communities (89 shown, 29 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 378 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0287abcf`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- extensions.py
- routes/students.py
- react
- Enrollment
- SessionStudent
- schemas/students.py
- schemas/attendance.py
- schemas/billing.py
- User
- AddTeacherModal.tsx
- tenant_required
- vinta-school-os/package.json
- billing.ts
- formatters.ts
- routes/settings.py
- Student
- ClassQuickCreate.tsx
- BillingPage.tsx
- formatters.py
- AcademySettings
- sessionLifecycle.ts
- SchedulingModal.tsx
- SessionMenu.tsx
- routes/calendar.py
- schemas/settings.py
- routes/attendance.py
- Teacher
- SessionCheckInModal.tsx
- routes/auth.py
- schemas/notifications.py
- env.py
- schemas/teachers.py
- TestCheckInFlow
- TestSessionCRUD
- compilerOptions
- cron_jobs.py
- Academy Root Entity
- constants.ts
- routes/classes.py
- routes/teachers.py
- schemas/classes.py
- CalendarPage.tsx
- api.ts
- SessionDetail.tsx
- StudentBilling
- Luxury School OS Concept
- Student
- PaymentHistoryList.tsx
- payroll_service.py
- ClassDetail.tsx
- ActivityLog.tsx
- StudentGuardians.tsx
- router.tsx
- cn
- compilerOptions
- TestAgingBuckets
- class.ts
- add_lifecycle_columns.py
- DashboardPage.tsx
- ActivityLog
- providers.tsx
- ClassesPage.tsx
- StudentAttendanceCalendar.tsx
- app/__init__.py
- Session
- test_cancel_session.py
- calendar.ts
- billing_service.py
- ClassGrid.tsx
- test_payroll_calc.py
- config.py
- schemas/calendar.py
- teacherEmails.ts
- Session
- TimePicker.tsx
- DayView.tsx
- WeekView.tsx
- Avatar.tsx
- C-01 Hardcoded Fallback JWT Secret Vulnerability
- datetime
- .oxlintrc.json
- uiStore.ts
- ErrorBoundary
- BillingSummaryCard.tsx
- audit_service.py
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
- student.ts
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
- `make_session()` --uses--> `Session`  [INFERRED]
  .tmp-relprobe/probe_audit_fk.py → Backend/vinta-academy-backend/app/models/scheduling.py
- `dbval()` --uses--> `AcademySettings`  [INFERRED]
  .tmp-relprobe/probe_billing_rules.py → Backend/vinta-academy-backend/app/models/academy.py
- `credits_of()` --uses--> `StudentSubscription`  [INFERRED]
  .tmp-relprobe/probe_finalise.py → Backend/vinta-academy-backend/app/models/billing.py
- `make_session()` --uses--> `Session`  [INFERRED]
  .tmp-relprobe/probe_finalise.py → Backend/vinta-academy-backend/app/models/scheduling.py
- `make_session()` --uses--> `Session`  [INFERRED]
  .tmp-relprobe/probe_start.py → Backend/vinta-academy-backend/app/models/scheduling.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Multi-Tenant Core Architecture & Domain Boundaries** — docs_documentation_tenant_isolation_model, docs_documentation_entity_academy, backend_api_architecture_overview, docs_documentation_billing_architecture [EXTRACTED 1.00]
- **Session Lifecycle & Attendance Grid Flow** — docs_documentation_entity_scheduled_session, docs_documentation_attendance_workflow, vinta_tasks_t1_session_lifecycle_lock, vinta_tasks_t2_false_until_true_attendance [INFERRED 0.85]

## Communities (118 total, 29 thin omitted)

### Community 0 - "extensions.py"
Cohesion: 0.07
Nodes (33): Vinta School OS — Extension Initialization Centralized extension instances for…, Vinta School OS — Activity Log & Audit Trail Model Every significant action is…, Vinta School OS — Scheduling Models Schedule (recurring weekly slot), Session…, Vinta School OS — User Model User (Owner/Staff) with PIN hashing, role…, Vinta School OS — Application Entry Point Launches the Flask application with…, bcrypt, flask_cors, flask_jwt_extended (+25 more)

### Community 1 - "routes/students.py"
Cohesion: 0.12
Nodes (26): Guardian, Student guardian / emergency contact. One student can have multiple guardians., add_guardian(), bulk_enroll_students(), create_student(), delete_student(), enroll_student(), get_stats() (+18 more)

### Community 2 - "react"
Cohesion: 0.07
Nodes (48): lucide-react, react, react-router-dom, Badge, Button, ButtonProps, sizeStyles, variantStyles (+40 more)

### Community 3 - "Enrollment"
Cohesion: 0.15
Nodes (13): Enrollment, Many-to-many: Student ↔ Class through Enrollment., create_multi_payment(), create_subscription(), create_subscription_for_payment(), MultiPaymentError, Exception, Create a subscription for a payment covering a course group. Args:… (+5 more)

### Community 4 - "SessionStudent"
Cohesion: 0.05
Nodes (63): Many-to-many: Session ↔ Student. Tracks attendance (is_present, check-in/out…, SessionStudent, absence_consumes_credit(), count_gap_sessions(), early_payment_on_extra_sessions(), free_session_auto_present(), Vinta School OS — Academy Rules Per-academy policy, read at the moment a…, The academy's settings row, or None if it has never been created. (+55 more)

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
Cohesion: 0.05
Nodes (48): Every person who logs into the system. Owner or Staff., Hash a 4-digit PIN using bcrypt., Verify a PIN against the stored hash., Hash a password using bcrypt., Verify a password against the stored hash., Set a new password hash (owner only)., User, create_owner() (+40 more)

### Community 9 - "AddTeacherModal.tsx"
Cohesion: 0.10
Nodes (22): DayPicker(), DayPickerProps, sizeStyles, todayISO(), toISO(), WEEKDAYS, AddTeacherModalProps, COMMISSION_PLACEHOLDER (+14 more)

### Community 10 - "tenant_required"
Cohesion: 0.11
Nodes (41): check_overdue(), create_plan(), finalize_session(), get_aging_buckets(), get_revenue(), get_revenue_chart(), get_stats(), list_payouts() (+33 more)

### Community 11 - "vinta-school-os/package.json"
Cohesion: 0.04
Nodes (44): axios, clsx, oxlint, ref_path, recharts, tailwind-merge, tailwindcss, @tailwindcss/vite (+36 more)

### Community 12 - "billing.ts"
Cohesion: 0.10
Nodes (19): AgingBucket, BillingRingData, BillingState, BillingStats, CreatePaymentPlanRequest, GroupCharge, MultiPayReceipt, MultiPayRequest (+11 more)

### Community 13 - "formatters.ts"
Cohesion: 0.20
Nodes (12): AgendaBoard(), hexToRgba(), resolveOverlaps(), SessionDetail, formatDateISO(), formatTime12(), getCurrentHour(), getDayName() (+4 more)

### Community 14 - "routes/settings.py"
Cohesion: 0.08
Nodes (49): add_staff(), _coerce_bool(), deactivate_staff(), delete_staff(), export_data(), get_academy(), get_activity_log(), get_appearance() (+41 more)

### Community 15 - "Student"
Cohesion: 0.06
Nodes (50): Student purchase of a Class offer (credit-based or time-based). Table name is…, StudentSubscription, A child enrolled in the academy., Student, get_billing_stats(), list_subscriptions(), List student subscriptions with optional filters., Get aggregate billing statistics for the donut chart. Uses the new… (+42 more)

### Community 16 - "ClassQuickCreate.tsx"
Cohesion: 0.19
Nodes (16): buildClassPayload(), CLASS_COLOR_PRESETS, ClassBillingFields(), classCancelBtnCls, ClassFormValues, classInputCls, classLabelCls, classSubmitBtnCls (+8 more)

### Community 17 - "BillingPage.tsx"
Cohesion: 0.07
Nodes (37): BillingPage, BadgeProps, SemanticVariant, sizeStyles, variantAliases, variantStyles, BillingPage(), BillingTab (+29 more)

### Community 18 - "formatters.py"
Cohesion: 0.10
Nodes (23): days_until(), format_dzd(), format_phone(), month_date_range(), next_occurrence(), now_utc(), parse_dzd(), date (+15 more)

### Community 19 - "AcademySettings"
Cohesion: 0.05
Nodes (44): Academy, AcademySettings, Academy SaaS subscription tier., Top-level tenant entity. One academy = one private school/academy., Per-academy configuration singleton., Subscription, PaymentPlan, Reusable billing plans that can be assigned to students. (+36 more)

### Community 20 - "sessionLifecycle.ts"
Cohesion: 0.18
Nodes (21): ClassCardMenu(), isRunning(), canStart(), canStartSession(), getEffectiveStatus(), getLifecycleRecord(), getScheduledDateTime(), getScheduledEnd() (+13 more)

### Community 21 - "SchedulingModal.tsx"
Cohesion: 0.10
Nodes (35): errMsg(), GroupOption, inputCls, Mode, primaryBtnCls, RoomOption, SchedulingModal(), TeacherOption (+27 more)

### Community 22 - "SessionMenu.tsx"
Cohesion: 0.07
Nodes (40): Select, SelectAction, SelectOption, SelectProps, dangerBtnCls, FinancesModal(), FreeNextModal(), inputCls (+32 more)

### Community 23 - "routes/calendar.py"
Cohesion: 0.11
Nodes (28): add_student_to_session(), cancel_session(), create_session(), _duration_label(), end_session(), get_day(), get_session_roster(), get_week() (+20 more)

### Community 24 - "schemas/settings.py"
Cohesion: 0.08
Nodes (34): AcademyResponseSchema, AddStaffRequestSchema, AddStaffResponseSchema, AppearanceResponseSchema, AutomationsResponseSchema, BillingConfigResponseSchema, ProfileResponseSchema, Schema (+26 more)

### Community 25 - "routes/attendance.py"
Cohesion: 0.12
Nodes (24): add_to_session(), auto_checkout(), check_in(), check_out(), complete_session(), get_roster(), guest_check_in(), jwt_required (+16 more)

### Community 26 - "Teacher"
Cohesion: 0.15
Nodes (12): An instructor employed by the academy., Teacher, export_chart_data(), export_teacher_hours(), Generate CSV for chart data based on chart type. Supports: income, enrollments,…, Generate CSV for teacher hours. Columns: Teacher, Session, Date, Hours, Subject, get_teacher_payout_dashboard(), get_teacher_summary() (+4 more)

### Community 27 - "SessionCheckInModal.tsx"
Cohesion: 0.09
Nodes (43): RosterEntry, SessionCheckInModal(), STATUS_CONFIG, StudentSearchResult, DangerConfirmModal(), VoidModal(), BILLING_RULE_DEFAULTS, BILLING_RULE_FIELDS (+35 more)

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

### Community 32 - "TestCheckInFlow"
Cohesion: 0.08
Nodes (18): integration, Test session roster operations., New session should have empty roster., Should be able to add a student to a session roster., Adding the same student twice should return existing record., Test auto-checkout trigger., Test student check-in to session., Auto-checkout should check out all present students. (+10 more)

### Community 33 - "TestSessionCRUD"
Cohesion: 0.07
Nodes (17): integration, Should update session date via PATCH., Moved session times should snap to 5-minute grid., Should cancel a session via DELETE., Test recurring schedule → session generation., Test session create/read/update/delete via API., Creating a schedule should auto-generate sessions for 12 weeks., Should create a new session with valid data. (+9 more)

### Community 34 - "compilerOptions"
Cohesion: 0.07
Nodes (26): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, baseUrl, erasableSyntaxOnly, forceConsistentCasingInFileNames, ignoreDeprecations, isolatedModules (+18 more)

### Community 35 - "cron_jobs.py"
Cohesion: 0.13
Nodes (22): Create new billing records for students whose cycles have ended. Returns count…, renew_billing_cycles(), auto_checkout_expired_sessions(), Vinta School OS — Cron Jobs Automated check-outs, overdue status checks,…, Create new billing records for students whose cycles have ended. Runs daily at…, Check all in-progress sessions whose end_time has passed and auto check-out any…, renew_billing_cycles(), _make_session() (+14 more)

### Community 36 - "Academy Root Entity"
Cohesion: 0.09
Nodes (25): Attendance Blueprint (/api/attendance), Billing & Subscriptions Blueprint (/api/billing), Calendar & Sessions Blueprint (/api/sessions), Classes & Groups Blueprint (/api/classes), Students Blueprint (/api/students), Teachers Blueprint (/api/teachers), Session Attendance & Check-in/out Flow, Student Tuition & Credit/Time Billing Architecture (+17 more)

### Community 37 - "constants.ts"
Cohesion: 0.08
Nodes (24): ACADEMY_ID_KEY, ACTIVITY_TYPES, API_BASE_URL, AvatarPreset, BREAKPOINTS, CHART_COLORS, DEFAULT_SESSION_DURATION, ENTITY_FILTER_PAGES (+16 more)

### Community 38 - "routes/classes.py"
Cohesion: 0.06
Nodes (69): Class, A subject offering (e.g., 'Math — CM2'). Enrollment target for students., Recurring weekly slot defining when a class meets., Schedule, _apply_group_fields(), create_class(), create_classroom(), create_schedule() (+61 more)

### Community 39 - "routes/teachers.py"
Cohesion: 0.13
Nodes (26): Junction table for teacher-subject many-to-many relationship., TeacherSubject, _clean_email(), _clean_status(), create_teacher(), delete_teacher(), _email_taken(), get_stats() (+18 more)

### Community 40 - "schemas/classes.py"
Cohesion: 0.12
Nodes (24): ClassListResponseSchema, ClassListSchema, ClassroomListResponseSchema, ClassroomSchema, CreateClassRequestSchema, CreateClassResponseSchema, CreateClassroomRequestSchema, CreateScheduleRequestSchema (+16 more)

### Community 41 - "CalendarPage.tsx"
Cohesion: 0.13
Nodes (25): CalendarPage(), hourLabel(), errMsg(), GroupOption, inputCls, RoomOption, SessionWindowModal(), TeacherOption (+17 more)

### Community 42 - "api.ts"
Cohesion: 0.08
Nodes (26): StudentsPage, NotificationBell(), relativeTime(), styleFor(), TYPE_STYLE, AddStudentModal(), AddStudentModalProps, ClassOption (+18 more)

### Community 43 - "SessionDetail.tsx"
Cohesion: 0.10
Nodes (22): PINInput, PINInputProps, PinStepProps, SessionActions(), InfoChipProps, SessionDetailProps, STATUS_BADGE_CLASSES, StudentRow() (+14 more)

### Community 44 - "StudentBilling"
Cohesion: 0.07
Nodes (32): PaymentLog, One record per billing cycle per student. Core billing entity., Individual payment transactions against a billing record., StudentBilling, export_data(), get_dashboard(), jwt_required, route (+24 more)

### Community 45 - "Luxury School OS Concept"
Cohesion: 0.11
Nodes (19): Flask REST API Architecture, Auth Blueprint (/api/auth), Two-Stage Auth & Profile PIN Verification Flow, Docker Compose Local Environment, Flask & SQLAlchemy Dependencies, PIN-Attributed Activity Log & Audit Trail, Algerian Private Academy Target Market, Glassmorphic Design Tokens (--gold / --emerald) (+11 more)

### Community 46 - "Student"
Cohesion: 0.16
Nodes (17): MultiPayModalProps, BillingSummaryCardProps, STUDENT_STATUS_LABELS, safePhone(), StudentIdentity(), StudentIdentityProps, UseStudentProfileResult, StudentDrawerProps (+9 more)

### Community 47 - "PaymentHistoryList.tsx"
Cohesion: 0.26
Nodes (11): humaniseStatus(), METHOD_LABELS, methodLabel(), parseTimestamp(), PaymentHistoryList(), PaymentHistoryListProps, purchaseShape(), statusPillClasses() (+3 more)

### Community 48 - "payroll_service.py"
Cohesion: 0.10
Nodes (21): Monthly payroll record for each teacher., TeacherPayroll, calculate_payout_for_session(), generate_monthly_payroll(), list_payouts(), list_teacher_payrolls(), log_teacher_hours(), mark_paid() (+13 more)

### Community 49 - "ClassDetail.tsx"
Cohesion: 0.14
Nodes (16): ClassBillingStat(), fetchBilling(), ClassDetail(), COLOR_PRESETS, DAY_LABELS, DAY_SHORT, EnrolledStudent, getScheduleBounds() (+8 more)

### Community 50 - "ActivityLog.tsx"
Cohesion: 0.18
Nodes (10): ActivityLog, ActivityLogEntry, ActivityLogProps, ActivityRow(), ActivityRowProps, ICON_MAP, ICON_STYLE, relativeTime() (+2 more)

### Community 51 - "StudentGuardians.tsx"
Cohesion: 0.20
Nodes (12): EmptyLine(), InlineSpinner(), ProfileCard(), ProfileCardProps, StudentClasses(), StudentClassesProps, GuardianRow, safePhone() (+4 more)

### Community 52 - "router.tsx"
Cohesion: 0.05
Nodes (56): AppShell(), AuthGuard(), AuthScreen, CalendarPage, DashboardPage, ProfileCreator, ProfileGuard(), ProfilePicker (+48 more)

### Community 53 - "cn"
Cohesion: 0.07
Nodes (36): PageContainer(), PageContainerProps, CardFooter, ConfirmDialog, Drawer, DrawerProps, EmptyState(), maxWidthMap (+28 more)

### Community 54 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 55 - "TestAgingBuckets"
Cohesion: 0.09
Nodes (15): unit, Should return 0 for future due dates., Should return 0 when due date is today., Test payment plan creation and properties., Payment plans should store correct values., Term plans should have 90-day duration., Test aging bucket classification., 1-7 days overdue should be classified as 'recent'. (+7 more)

### Community 56 - "class.ts"
Cohesion: 0.12
Nodes (16): RosterStudent, AttendanceStatus, CheckInRequest, ClassBillingInfo, Classroom, ClassState, ClassStats, CreateClassRequest (+8 more)

### Community 57 - "add_lifecycle_columns.py"
Cohesion: 0.16
Nodes (11): main(), Additive migration — billing relations, session lifecycle, billing toggles.…, Resolve the SQLite file the app actually opens, from DATABASE_URL., resolve_db_path(), One-shot database fix — adds any missing columns to existing tables. Run once:…, main(), Schema step — activity_logs.user_id becomes nullable. WHY The audit trail has…, Resolve the SQLite file the app actually opens, from DATABASE_URL. (+3 more)

### Community 58 - "DashboardPage.tsx"
Cohesion: 0.18
Nodes (16): calendarRequest(), DashboardPage(), load(), loadStats(), getWeekRange(), isToday(), StatCard, SessionMenu() (+8 more)

### Community 59 - "ActivityLog"
Cohesion: 0.12
Nodes (17): ActivityLog, Audit trail. Every significant action in the system is logged with user_id —…, add_student_to_session(), check_out_student(), get_session_roster(), get_session_roster_with_badges(), Vinta School OS — Attendance Service Manual check-in, auto-checkout at class…, Check out a student from a session. (+9 more)

### Community 60 - "providers.tsx"
Cohesion: 0.12
Nodes (13): react-dom, App(), Providers(), ProvidersProps, TOAST_COLORS, TOAST_ICONS, ToastContainer(), AppRouter() (+5 more)

### Community 61 - "ClassesPage.tsx"
Cohesion: 0.12
Nodes (15): ClassesPage, AddClassroomModal(), AddCourseGroupModal(), cancelBtnCls, ClassesPage(), ClassroomList(), COLOR_PRESETS, inputCls (+7 more)

### Community 62 - "StudentAttendanceCalendar.tsx"
Cohesion: 0.23
Nodes (11): dominantState(), formatTime(), monthCells(), STATE_PRIORITY, STATE_STYLES, StateStyle, StudentAttendanceCalendar(), StudentAttendanceCalendarProps (+3 more)

### Community 63 - "app/__init__.py"
Cohesion: 0.10
Nodes (15): Fail fast if critical secrets are not configured., validate_config(), create_app(), check_if_token_revoked(), Vinta School OS — Application Factory Creates and configures the Flask…, Application factory pattern., Register shell context objects., Register all API blueprints. (+7 more)

### Community 64 - "Session"
Cohesion: 0.15
Nodes (14): DayViewProps, FinalizeSessionModalProps, SchedulingModalProps, SessionCheckInModalProps, SessionWindowModalProps, ClassCardMenuProps, CreatedGroup, AgendaBoardProps (+6 more)

### Community 65 - "test_cancel_session.py"
Cohesion: 0.16
Nodes (21): cancel_session(), Cancel a session, recording *why*. The reason is not decoration:…, Vinta School OS — cancelling a session. ``cancel_session`` is reached from…, CANCEL_REASONS is a plain Python tuple; the column is a native enum that knows…, An unrecognised reason is a label problem, not a reason to lose the cancel., A bare DELETE still cancels; it just does not claim to know why., Tenant scoping — the lookup is by id AND academy., A class that has not run can be called off; a class that is running can be… (+13 more)

### Community 66 - "calendar.ts"
Cohesion: 0.19
Nodes (12): hexToRgba(), SessionBlock(), SessionBlockProps, formatTime(), CalendarSession, CalendarState, CalendarViewMode, CreateSessionData (+4 more)

### Community 67 - "billing_service.py"
Cohesion: 0.05
Nodes (47): PayoutRecord, Immutable revenue fact per conducted session allocation (DZD integers)., Teacher payout computed from gross revenue per conducted session., RevenueEntry, check_in_student(), Mark a student as checked in to a session. Args: session_id: session being…, _compute_teacher_cut(), finalize_session() (+39 more)

### Community 68 - "ClassGrid.tsx"
Cohesion: 0.26
Nodes (12): ClassDetailProps, ClassCard(), ClassCardProps, ClassGridProps, resolveColor(), SkeletonCard(), statusDotColor(), statusLabel() (+4 more)

### Community 69 - "test_payroll_calc.py"
Cohesion: 0.15
Nodes (14): Records when a teacher's hours are logged (per session)., TeacherHoursLog, calculate_teacher_payroll(), date, Calculate payroll for a teacher for a given period. Hourly: total_hours ×…, unit, Unit Tests — Teacher Payroll Calculations Tests for hourly vs per-student…, Test hourly contract payroll calculations. (+6 more)

### Community 70 - "config.py"
Cohesion: 0.24
Nodes (10): BaseConfig, DevelopmentConfig, ProductionConfig, Vinta School OS — Configuration Environments Dev, Test, and Production…, Shared configuration across all environments., Development environment configuration., Test environment configuration., Production environment configuration. (+2 more)

### Community 71 - "schemas/calendar.py"
Cohesion: 0.17
Nodes (15): CreateSessionRequestSchema, CreateSessionResponseSchema, DaySessionsResponseSchema, Schema, Calendar schemas — Session CRUD, Week/Day views, Drag-and-drop., PATCH /api/sessions/<id>, Single session in calendar view., GET /api/calendar/week response. (+7 more)

### Community 72 - "teacherEmails.ts"
Cohesion: 0.33
Nodes (9): RFC-5322, currentAcademy(), getTeacherEmail(), isValidEmail(), listTeacherEmails(), loadAll(), saveAll(), setTeacherEmail() (+1 more)

### Community 73 - "Session"
Cohesion: 0.24
Nodes (11): A concrete class session on a specific date. Generated from Schedule or created…, Session, get_class_sessions(), get_day_sessions(), get_week_sessions(), date, Serialize a session to a dict for API response. The lifecycle fields are part…, Get all sessions for a given week. (+3 more)

### Community 74 - "TimePicker.tsx"
Cohesion: 0.31
Nodes (8): Column(), formatLabel(), HOURS, minutesFor(), parse(), sizeStyles, TimePicker(), TimePickerProps

### Community 75 - "DayView.tsx"
Cohesion: 0.42
Nodes (8): DayView(), decimalToTime(), snapHour(), toCalendarSession(), yToTime(), CALENDAR_HOURS, HOUR_HEIGHT, formatHour12()

### Community 76 - "WeekView.tsx"
Cohesion: 0.50
Nodes (8): decimalToTime(), snapHour(), toCalendarSession(), WeekView(), xToDayIndex(), yToTime(), getWeekDates(), timeToDecimal()

### Community 77 - "Avatar.tsx"
Cohesion: 0.33
Nodes (8): Avatar, AvatarProps, getGradientForName(), getInitials(), gradientPairs, hashCode(), sizeConfig, squircleRadius()

### Community 81 - "datetime"
Cohesion: 0.09
Nodes (27): Vinta School OS — Academy & Tenant Models Academy (tenant root),…, Vinta School OS — Attendance Model SessionStudent: tracks check-in/out per…, Vinta School OS — Billing Models PaymentPlan, StudentBilling, PaymentLog…, Vinta School OS — Classroom, Class & Subject Models Classroom (physical room),…, Vinta School OS — Model Exports Centralized imports for Flask-Migrate and…, Vinta School OS — Notification Model In-app toast notifications and alerts., Vinta School OS — Student Models Student, Guardian (1:N), Enrollment (M:N with…, Vinta School OS — Teacher Models Teacher, TeacherPayroll, TeacherHoursLog. (+19 more)

### Community 83 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 84 - "uiStore.ts"
Cohesion: 0.10
Nodes (24): TeachersPage, FinalizeSessionModal(), commissionBadgeLabel(), commissionRateLabel(), DAYS, editInputCls, generateWeeklySchedule(), PayrollStat() (+16 more)

### Community 85 - "ErrorBoundary"
Cohesion: 0.22
Nodes (3): ErrorBoundary, Props, State

### Community 86 - "BillingSummaryCard.tsx"
Cohesion: 0.26
Nodes (12): BillingCalendarCard(), BillingCalendarCardProps, CYCLE_STATUS_LABELS, statusDot(), BillingSummaryCard(), DASH, formatDateRange(), formatDisplayDate() (+4 more)

### Community 87 - "audit_service.py"
Cohesion: 0.22
Nodes (9): get_activity_logs(), get_log_count(), log_action(), _map_log_type(), Vinta School OS — Audit Service Staff PIN attribution logger, activity log…, Get total activity log count for an academy., Create an attributed activity log entry. Every action is attributed to the…, Get activity logs for an academy, newest first. UI shows last 30 entries with… (+1 more)

### Community 117 - "student.ts"
Cohesion: 0.25
Nodes (7): AttendanceCalendar, AttendanceDayState, CreateGuardianRequest, CreateStudentRequest, StudentState, StudentStats, UpdateStudentRequest

### Community 118 - "conftest.py"
Cohesion: 0.10
Nodes (19): Classroom, Extensible palette entity for calendar subject colors., A physical room in the academy., Subject, app(), auth_headers_owner(), auth_headers_staff(), classroom() (+11 more)

### Community 119 - "routes/notifications.py"
Cohesion: 0.13
Nodes (22): Notification, In-app toast notification / alert., create_notification(), get_unread_count(), list_notifications(), mark_all_read(), mark_read(), jwt_required (+14 more)

### Community 121 - "themeStore.ts"
Cohesion: 0.17
Nodes (17): FONT_SIZE_KEY, LANGUAGE_KEY, THEME_KEY, applyFontSize(), applyLanguage(), applyTheme(), FontSize, Language (+9 more)

### Community 124 - "marshmallow"
Cohesion: 0.29
Nodes (7): DashboardResponseSchema, Schema, Analytics schemas — Dashboard stats, Revenue chart, CSV export., GET /api/analytics/revenue-chart response., GET /api/analytics/dashboard response., RevenueChartResponseSchema, marshmallow

## Knowledge Gaps
- **384 isolated node(s):** `type`, `Meta`, `$schema`, `plugins`, `react/rules-of-hooks` (+379 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1137 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **29 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `tenant_required()` connect `tenant_required` to `routes/students.py`, `routes/classes.py`, `routes/teachers.py`, `User`, `StudentBilling`, `routes/settings.py`, `AcademySettings`, `routes/calendar.py`, `routes/notifications.py`, `routes/attendance.py`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Why does `Session` connect `Session` to `extensions.py`, `SessionStudent`, `routes/settings.py`, `Student`, `routes/calendar.py`, `routes/attendance.py`, `Teacher`, `TestSessionCRUD`, `cron_jobs.py`, `routes/classes.py`, `routes/teachers.py`, `StudentBilling`, `payroll_service.py`, `ActivityLog`, `test_cancel_session.py`, `billing_service.py`, `test_payroll_calc.py`, `datetime`, `conftest.py`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Why does `cn()` connect `cn` to `react`, `AddTeacherModal.tsx`, `formatters.ts`, `ClassQuickCreate.tsx`, `BillingPage.tsx`, `SchedulingModal.tsx`, `SessionMenu.tsx`, `SessionCheckInModal.tsx`, `CalendarPage.tsx`, `api.ts`, `SessionDetail.tsx`, `Student`, `PaymentHistoryList.tsx`, `ClassDetail.tsx`, `ActivityLog.tsx`, `StudentGuardians.tsx`, `router.tsx`, `DashboardPage.tsx`, `providers.tsx`, `ClassesPage.tsx`, `StudentAttendanceCalendar.tsx`, `calendar.ts`, `ClassGrid.tsx`, `TimePicker.tsx`, `DayView.tsx`, `WeekView.tsx`, `Avatar.tsx`, `uiStore.ts`, `BillingSummaryCard.tsx`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `tenant_required()` (e.g. with `Academy` and `User`) actually correct?**
  _`tenant_required()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 40 inferred relationships involving `Session` (e.g. with `get_dashboard()` and `get_roster()`) actually correct?**
  _`Session` has 40 INFERRED edges - model-reasoned connections that need verification._
- **What connects `type`, `Meta`, `$schema` to the rest of the system?**
  _384 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `extensions.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07337662337662337 - nodes in this community are weakly interconnected._