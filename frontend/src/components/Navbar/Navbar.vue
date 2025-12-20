<template>
	<!-- Edison Template Style Header -->
	<header class="header" data-page="home">
		<div class="header-container">
			<!-- Logo -->
			<div class="logo header_logo">
				<router-link to="/" class="logo-link">
					<span class="logo_picture">
						<img
							v-if="branding.data?.banner_image"
							:src="branding.data.banner_image.file_url"
							:alt="brandName"
						/>
						<LMSLogo v-else class="logo-img" />
					</span>
					<span class="logo-text">
						<span class="brand">{{ brandName }}</span>
						<span class="text_secondary">courses</span>
					</span>
				</router-link>
			</div>

			<!-- Mobile menu button -->
			<button class="header_trigger" type="button" @click="showMobileMenu = !showMobileMenu">
				<span class="line"></span>
				<span class="line"></span>
				<span class="line"></span>
			</button>

			<!-- Navigation -->
			<nav class="header_nav" :class="{ 'show': showMobileMenu }">
				<ul class="header_nav-list">
					<li class="header_nav-list_item">
						<router-link
							to="/"
							class="nav-item"
							:class="{ 'active': isActive('Home') }"
							@click="showMobileMenu = false"
						>
							Home
						</router-link>
					</li>
					<li class="header_nav-list_item dropdown">
						<a
							class="nav-item dropdown-toggle"
							href="#"
							@click.prevent="toggleDropdown('courses')"
							:class="{ 'active': isActive('Courses') || isActive('CourseDetail') }"
						>
							Courses
							<i class="icon-angle-down"></i>
						</a>
						<div class="dropdown-menu" :class="{ 'show': openDropdown === 'courses' }">
							<ul class="dropdown-list">
								<li class="list-item">
									<router-link
										to="/courses"
										class="dropdown-item nav-item"
										@click="closeDropdowns"
									>
										All Courses
									</router-link>
								</li>
								<li class="list-item">
									<router-link
										to="/batches"
										class="dropdown-item nav-item"
										@click="closeDropdowns"
									>
										Batches
									</router-link>
								</li>
								<li class="list-item">
									<router-link
										to="/certified-participants"
										class="dropdown-item nav-item"
										@click="closeDropdowns"
									>
										Certifications
									</router-link>
								</li>
							</ul>
						</div>
					</li>
					<li class="header_nav-list_item">
						<router-link
							to="/job-openings"
							class="nav-item"
							:class="{ 'active': isActive('Jobs') || isActive('JobDetail') }"
							@click="showMobileMenu = false"
						>
							Jobs
						</router-link>
					</li>
					<li class="header_nav-list_item">
						<router-link
							to="/statistics"
							class="nav-item"
							:class="{ 'active': isActive('Statistics') }"
							@click="showMobileMenu = false"
						>
							Statistics
						</router-link>
					</li>
					<!-- More menu for logged in users -->
					<li v-if="isLoggedIn" class="header_nav-list_item dropdown">
						<a
							class="nav-item dropdown-toggle"
							href="#"
							@click.prevent="toggleDropdown('more')"
						>
							More
							<i class="icon-angle-down"></i>
						</a>
						<div class="dropdown-menu" :class="{ 'show': openDropdown === 'more' }">
							<ul class="dropdown-list">
								<li class="list-item">
									<router-link
										to="/programs"
										class="dropdown-item nav-item"
										@click="closeDropdowns"
									>
										Programs
									</router-link>
								</li>
								<li class="list-item">
									<router-link
										to="/notifications"
										class="dropdown-item nav-item"
										@click="closeDropdowns"
									>
										Notifications
									</router-link>
								</li>
								<li v-if="isModerator || isInstructor" class="list-item">
									<router-link
										to="/quizzes"
										class="dropdown-item nav-item"
										@click="closeDropdowns"
									>
										Quizzes
									</router-link>
								</li>
								<li v-if="isModerator || isInstructor" class="list-item">
									<router-link
										to="/assignments"
										class="dropdown-item nav-item"
										@click="closeDropdowns"
									>
										Assignments
									</router-link>
								</li>
							</ul>
						</div>
					</li>
				</ul>

				<!-- Auth buttons / User menu -->
				<div class="header-auth">
					<!-- Guest: Show Sign Up and Log In -->
					<template v-if="!isLoggedIn">
						<a href="/login#signup" class="btn-auth btn-auth-signup">Sign Up</a>
						<a href="/login" class="btn-auth btn-auth-login">Log In</a>
					</template>

					<!-- Logged in: Show user menu -->
					<div v-else class="user-menu">
						<a href="#" class="user-trigger" @click.prevent="toggleDropdown('user')">
							<img
								v-if="userResource.data?.user_image"
								:src="userResource.data.user_image"
								class="user-avatar"
								:alt="userResource.data?.full_name"
							/>
							<div v-else class="user-avatar user-avatar-placeholder">
								{{ userInitial }}
							</div>
						</a>
						<div class="user-dropdown" :class="{ 'show': openDropdown === 'user' }">
							<div class="user-info">
								<span class="user-name">{{ userResource.data?.full_name }}</span>
								<span class="user-email">{{ userResource.data?.email }}</span>
							</div>
							<div class="dropdown-divider"></div>
							<router-link
								:to="`/user/${userResource.data?.username}`"
								class="dropdown-link"
								@click="closeDropdowns"
							>
								<i class="icon-user"></i> My Profile
							</router-link>
							<a
								v-if="isSystemUser"
								href="/app"
								class="dropdown-link"
							>
								<i class="icon-th-large"></i> Switch to Desk
							</a>
							<button
								v-if="userResource.data?.is_moderator"
								@click="openSettings"
								class="dropdown-link"
							>
								<i class="icon-cog"></i> Settings
							</button>
							<div class="dropdown-divider"></div>
							<button @click="handleLogout" class="dropdown-link logout">
								<i class="icon-sign-out"></i> Log Out
							</button>
						</div>
					</div>
				</div>
			</nav>
		</div>
	</header>

	<!-- Settings modal -->
	<SettingsModal
		v-if="userResource.data?.is_moderator"
		v-model="showSettingsModal"
	/>
</template>

<script setup>
import { ref, computed, onMounted, watch, inject, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { createResource } from 'frappe-ui'
import { sessionStore } from '@/stores/session'
import { usersStore } from '@/stores/user'
import { useSettings } from '@/stores/settings'
import LMSLogo from '@/components/Icons/LMSLogo.vue'
import SettingsModal from '@/components/Settings/Settings.vue'

const router = useRouter()
const route = useRoute()
const { logout, branding, user } = sessionStore()
let { isLoggedIn } = sessionStore()
const { userResource } = usersStore()
const settingsStore = useSettings()

const showMobileMenu = ref(false)
const openDropdown = ref(null)
const showSettingsModal = ref(false)
const isModerator = ref(false)
const isInstructor = ref(false)

const brandName = computed(() => {
	return branding.data?.app_name && branding.data?.app_name !== 'Frappe'
		? branding.data.app_name
		: 'Learning'
})

const userInitial = computed(() => {
	return userResource.data?.full_name?.[0] || 'U'
})

const isSystemUser = computed(() => {
	const cookies = new URLSearchParams(document.cookie.split('; ').join('&'))
	return cookies.get('system_user') === 'yes'
})

const isActive = (name) => {
	return route.name === name
}

const toggleDropdown = (name) => {
	openDropdown.value = openDropdown.value === name ? null : name
}

const closeDropdowns = () => {
	openDropdown.value = null
	showMobileMenu.value = false
}

const openSettings = () => {
	closeDropdowns()
	settingsStore.isSettingsOpen = true
}

const handleLogout = () => {
	logout.submit().then(() => {
		isLoggedIn = false
		closeDropdowns()
	})
}

// Close dropdowns when clicking outside
const handleClickOutside = (e) => {
	if (!e.target.closest('.dropdown') && !e.target.closest('.user-menu')) {
		openDropdown.value = null
	}
}

onMounted(() => {
	document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
	document.removeEventListener('click', handleClickOutside)
})

watch(userResource, () => {
	if (userResource.data) {
		isModerator.value = userResource.data.is_moderator
		isInstructor.value = userResource.data.is_instructor
	}
})

watch(() => settingsStore.isSettingsOpen, (value) => {
	showSettingsModal.value = value
})
</script>

<style scoped>
/* Edison Template Style Navbar */
.header {
	background: #fff;
	box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
	position: sticky;
	top: 0;
	z-index: 1000;
}

.header-container {
	max-width: 1200px;
	margin: 0 auto;
	padding: 0 20px;
	display: flex;
	align-items: center;
	justify-content: space-between;
	height: 70px;
}

/* Logo */
.logo-link {
	display: flex;
	align-items: center;
	gap: 10px;
	text-decoration: none;
}

.logo_picture {
	width: 40px;
	height: 40px;
	display: flex;
	align-items: center;
	justify-content: center;
}

.logo_picture img,
.logo-img {
	width: 100%;
	height: 100%;
	object-fit: contain;
}

.logo-text {
	display: flex;
	flex-direction: column;
}

.logo-text .brand {
	font-size: 18px;
	font-weight: 700;
	color: #1a1a2e;
	line-height: 1.2;
}

.logo-text .text_secondary {
	font-size: 12px;
	color: #666;
	text-transform: uppercase;
	letter-spacing: 1px;
}

/* Navigation */
.header_nav {
	display: flex;
	align-items: center;
	gap: 30px;
}

.header_nav-list {
	display: flex;
	align-items: center;
	gap: 5px;
	list-style: none;
	margin: 0;
	padding: 0;
}

.header_nav-list_item {
	position: relative;
}

.nav-item {
	display: inline-flex;
	align-items: center;
	gap: 5px;
	padding: 10px 15px;
	font-size: 15px;
	font-weight: 500;
	color: #1a1a2e;
	text-decoration: none;
	position: relative;
	transition: color 0.3s;
}

.nav-item:hover {
	color: #ff0844;
}

.nav-item.active {
	color: #ff0844;
}

.nav-item.active::after {
	content: '';
	position: absolute;
	bottom: 0;
	left: 15px;
	right: 15px;
	height: 3px;
	background: linear-gradient(111.41deg, #ff0844 24.85%, #ff8b67 95.39%);
	border-radius: 2px;
}

.nav-item.dropdown-toggle::after {
	display: none;
}

.icon-angle-down {
	font-size: 12px;
	transition: transform 0.3s;
}

/* Dropdown */
.dropdown-menu {
	position: absolute;
	top: 100%;
	left: 0;
	background: #fff;
	border-radius: 8px;
	box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
	min-width: 180px;
	padding: 8px 0;
	opacity: 0;
	visibility: hidden;
	transform: translateY(10px);
	transition: all 0.3s;
	z-index: 100;
}

.dropdown-menu.show {
	opacity: 1;
	visibility: visible;
	transform: translateY(0);
}

.dropdown-list {
	list-style: none;
	margin: 0;
	padding: 0;
}

.dropdown-item {
	display: block;
	padding: 10px 20px;
	font-size: 14px;
	color: #1a1a2e;
	text-decoration: none;
	transition: background 0.2s;
}

.dropdown-item:hover {
	background: #f5f5f5;
}

/* Auth Buttons */
.header-auth {
	display: flex;
	align-items: center;
	gap: 10px;
}

.btn-auth {
	padding: 8px 22px;
	font-size: 13px;
	font-weight: 600;
	border-radius: 6px;
	text-decoration: none;
	transition: all 0.3s;
}

.btn-auth-signup {
	background: #f9d423;
	color: #1a1a2e;
}

.btn-auth-signup:hover {
	box-shadow: 0 4px 15px rgba(249, 212, 35, 0.4);
}

.btn-auth-login {
	background: transparent;
	color: #1a1a2e;
	border: 1.5px solid #1a1a2e;
}

.btn-auth-login:hover {
	background: #1a1a2e;
	color: #fff;
}

/* User Menu */
.user-menu {
	position: relative;
}

.user-trigger {
	display: block;
}

.user-avatar {
	width: 36px;
	height: 36px;
	border-radius: 50%;
	object-fit: cover;
	cursor: pointer;
}

.user-avatar-placeholder {
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	color: #fff;
	display: flex;
	align-items: center;
	justify-content: center;
	font-weight: 600;
	font-size: 14px;
}

.user-dropdown {
	position: absolute;
	top: calc(100% + 10px);
	right: 0;
	background: #fff;
	border-radius: 8px;
	box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
	min-width: 220px;
	padding: 10px 0;
	opacity: 0;
	visibility: hidden;
	transform: translateY(10px);
	transition: all 0.3s;
	z-index: 100;
}

.user-dropdown.show {
	opacity: 1;
	visibility: visible;
	transform: translateY(0);
}

.user-info {
	padding: 10px 15px;
}

.user-name {
	display: block;
	font-weight: 600;
	color: #1a1a2e;
	font-size: 14px;
}

.user-email {
	display: block;
	font-size: 12px;
	color: #666;
	margin-top: 2px;
}

.dropdown-divider {
	height: 1px;
	background: #eee;
	margin: 8px 0;
}

.dropdown-link {
	display: flex;
	align-items: center;
	gap: 10px;
	padding: 10px 15px;
	font-size: 14px;
	color: #1a1a2e;
	text-decoration: none;
	background: none;
	border: none;
	width: 100%;
	text-align: left;
	cursor: pointer;
	transition: background 0.2s;
}

.dropdown-link:hover {
	background: #f5f5f5;
}

.dropdown-link.logout {
	color: #e63946;
}

.dropdown-link i {
	width: 16px;
	text-align: center;
}

/* Mobile Menu Button */
.header_trigger {
	display: none;
	flex-direction: column;
	gap: 5px;
	padding: 10px;
	background: none;
	border: none;
	cursor: pointer;
}

.header_trigger .line {
	width: 24px;
	height: 2px;
	background: #1a1a2e;
	transition: all 0.3s;
}

/* Mobile Styles */
@media (max-width: 991px) {
	.header_trigger {
		display: flex;
	}

	.header_nav {
		position: fixed;
		top: 70px;
		left: 0;
		right: 0;
		background: #fff;
		flex-direction: column;
		padding: 20px;
		box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
		transform: translateY(-100%);
		opacity: 0;
		visibility: hidden;
		transition: all 0.3s;
		max-height: calc(100vh - 70px);
		overflow-y: auto;
	}

	.header_nav.show {
		transform: translateY(0);
		opacity: 1;
		visibility: visible;
	}

	.header_nav-list {
		flex-direction: column;
		width: 100%;
		gap: 0;
	}

	.header_nav-list_item {
		width: 100%;
	}

	.nav-item {
		width: 100%;
		padding: 12px 15px;
	}

	.nav-item.active::after {
		display: none;
	}

	.dropdown-menu {
		position: static;
		box-shadow: none;
		padding-left: 20px;
		opacity: 1;
		visibility: visible;
		transform: none;
		display: none;
	}

	.dropdown-menu.show {
		display: block;
	}

	.header-auth {
		width: 100%;
		flex-direction: column;
		margin-top: 15px;
		padding-top: 15px;
		border-top: 1px solid #eee;
	}

	.btn-auth {
		width: 100%;
		text-align: center;
	}

	.user-menu {
		width: 100%;
	}

	.user-dropdown {
		position: static;
		box-shadow: none;
		opacity: 1;
		visibility: visible;
		transform: none;
		display: none;
		min-width: 100%;
	}

	.user-dropdown.show {
		display: block;
	}
}
</style>
