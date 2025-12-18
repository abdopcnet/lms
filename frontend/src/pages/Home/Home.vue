<template>
	<div class="w-full px-5 pt-5 pb-10">
		<div class="space-y-2">
			<div class="flex items-center justify-between">
				<div class="text-xl font-bold text-ink-gray-9">
					{{ __('Hey') }}, {{ user.data?.full_name }} 👋
				</div>
				<div>
					<TabButtons v-if="isAdmin" v-model="currentTab" :buttons="tabs" />
					<div
						v-else
						@click="showStreakModal = true"
						class="bg-surface-amber-2 px-2 py-1 rounded-md cursor-pointer"
					>
						<span> 🔥 </span>
						<span class="text-ink-gray-9">
							{{ streakInfo.data?.current_streak }}
						</span>
					</div>
				</div>
			</div>
		</div>

		<!-- Hero Section -->
		<section
			class="relative w-full overflow-hidden text-center py-10 px-5 lg:text-left lg:py-20 lg:px-0"
		>
			<!-- Underlay background -->
			<div
				class="absolute inset-0 w-full h-full z-0 bg-gradient-to-br from-[rgba(251,248,254,0.0001)] to-[#fbf8fe]"
			></div>

			<div class="relative z-10 max-w-[1200px] mx-auto">
				<div
					class="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12 items-center"
				>
					<!-- Left Content -->
					<div class="hero_content space-y-6">
						<h1
							class="text-4xl md:text-5xl lg:text-6xl font-semibold leading-tight text-[#2b3543]"
							data-aos="fade-up"
						>
							Large educational programs
						</h1>
						<div
							class="flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-3"
						>
							<p
								class="text-base font-bold leading-relaxed text-[#3d53eb]"
								data-aos="fade-left"
							>
								Our course is rated excellent by over 42,000 people
							</p>
							<div
								class="flex items-center"
								data-aos="fade-left"
								data-aos-delay="50"
							>
								<ul class="flex items-center gap-1">
									<li v-for="i in 5" :key="i">
										<i class="icon-star icon text-[#f83600] text-base"></i>
									</li>
								</ul>
							</div>
						</div>
						<p
							class="text-base leading-relaxed text-[#485870]"
							data-aos="fade-up"
							data-aos-delay="50"
						>
							Today, more than 48,000 people have already studied at our
							university in various fields: programming, photography, marketing
							and management
						</p>
						<div
							class="flex flex-col sm:flex-row gap-4 pt-4"
							data-aos="fade-left"
						>
							<a
								class="relative overflow-hidden rounded-xl font-bold uppercase text-sm leading-none h-[54px] inline-flex items-center justify-center px-[30px] bg-gradient-to-br from-[#ff0844] to-[#ff8b67] text-white transition-all duration-300 hover:shadow-lg group w-full sm:w-auto"
								href="#"
							>
								<span class="relative z-10 text-sm leading-none">Sign Up</span>
								<div
									class="absolute inset-0 bg-gradient-to-br from-[#ff8b67] to-[#ff0844] opacity-0 transition-opacity duration-300 group-hover:opacity-100 z-0"
								></div>
							</a>
							<a
								class="relative overflow-hidden rounded-xl font-bold uppercase text-sm leading-none h-[54px] inline-flex items-center justify-center px-[30px] border-2 border-[#ff0844] text-[#ff0844] transition-all duration-300 group w-full sm:w-auto"
								href="pricing.html"
								data-aos="fade-left"
								data-aos-delay="50"
							>
								<span
									class="relative z-10 text-sm leading-none group-hover:text-white transition-colors duration-300"
									>See Pricing Plans</span
								>
								<div
									class="absolute inset-0 bg-gradient-to-br from-[#ff0844] to-[#ff8b67] opacity-0 transition-opacity duration-300 group-hover:opacity-100 z-0"
								></div>
							</a>
						</div>
					</div>

					<!-- Right Animation - Hero Image -->
					<div class="flex justify-center lg:justify-end w-full">
						<div
							class="w-full max-w-md lg:max-w-full h-80 lg:h-[500px] flex items-center justify-center relative overflow-hidden rounded-2xl bg-gradient-to-br from-blue-50 to-purple-50"
						>
							<!-- Background Image -->
							<img
								src="/img/home-bg.jpg"
								alt="Developer working"
								class="absolute inset-0 w-full h-full object-cover"
							/>
						</div>
					</div>
				</div>
			</div>
		</section>
	</div>

	<!-- Features Section -->
	<section class="py-20 px-5">
		<div class="max-w-[1200px] mx-auto">
			<div class="grid grid-cols-1 md:grid-cols-3 gap-8">
				<!-- Feature 1 -->
				<div
					class="bg-white rounded-2xl p-10 shadow-lg hover:shadow-2xl hover:-translate-y-2 transition-all duration-300 cursor-pointer group"
					data-aos="fade-up"
				>
					<div class="flex flex-col items-center text-center">
						<div
							class="w-24 h-24 bg-gradient-to-br from-purple-600 to-blue-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300"
						>
							<i class="icon-user-graduate-solid icon text-white text-4xl"></i>
						</div>
						<h5
							class="text-3xl font-bold text-gray-900 mb-4 group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-purple-600 group-hover:to-blue-600 transition-all duration-300"
						>
							Get a certificate
						</h5>
						<p class="text-gray-600 text-lg leading-relaxed">
							Sed a eros sodales diam sagittis faucibus. Cras id erat nisl.
							Lorem tempus rhoncus sit tortor.
						</p>
					</div>
				</div>

				<!-- Feature 2 -->
				<div
					class="bg-white rounded-2xl p-10 shadow-lg hover:shadow-2xl hover:-translate-y-2 transition-all duration-300 cursor-pointer group"
					data-aos="fade-up"
					data-aos-delay="50"
				>
					<div class="flex flex-col items-center text-center">
						<div
							class="w-24 h-24 bg-gradient-to-br from-purple-600 to-blue-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300"
						>
							<i class="icon-globe-solid icon text-white text-4xl"></i>
						</div>
						<h5
							class="text-3xl font-bold text-gray-900 mb-4 group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-purple-600 group-hover:to-blue-600 transition-all duration-300"
						>
							All over the globe
						</h5>
						<p class="text-gray-600 text-lg leading-relaxed">
							Donec urna massa, cursus venenatis ipsum et, tempus rhoncus
							tortor. Lorem ipsum dolor.
						</p>
					</div>
				</div>

				<!-- Feature 3 -->
				<div
					class="bg-white rounded-2xl p-10 shadow-lg hover:shadow-2xl hover:-translate-y-2 transition-all duration-300 cursor-pointer group"
					data-aos="fade-up"
					data-aos-delay="100"
				>
					<div class="flex flex-col items-center text-center">
						<div
							class="w-24 h-24 bg-gradient-to-br from-purple-600 to-blue-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300"
						>
							<i class="icon-headset-solid icon text-white text-4xl"></i>
						</div>
						<h5
							class="text-3xl font-bold text-gray-900 mb-4 group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-purple-600 group-hover:to-blue-600 transition-all duration-300"
						>
							Live online lectures
						</h5>
						<p class="text-gray-600 text-lg leading-relaxed">
							Sed a eros sodales diam sagittis faucibus. Cras id erat nisl.
							Lorem ipsum dolor sit lorem amet.
						</p>
					</div>
				</div>
			</div>
		</div>
	</section>

	<!-- About Section -->
	<section class="py-20 px-5 lg:py-32 bg-gradient-to-b from-blue-50 to-white">
		<div class="max-w-[1200px] mx-auto">
			<h2
				class="text-4xl md:text-5xl font-semibold text-gray-900 text-center mb-16"
				data-aos="fade-in"
			>
				How does it work?
			</h2>

			<div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
				<!-- Left - Steps -->

				<div class="space-y-8">
					<!-- Step 1 -->
					<div class="flex gap-4" data-aos="fade-up">
						<div class="flex-shrink-0">
							<div
								class="flex items-center justify-center h-10 w-10 rounded-full bg-gradient-to-br from-[#ff0844] to-[#ff8b67]"
							>
								<i class="icon-check icon text-white text-lg"></i>
							</div>
						</div>
						<div>
							<h5 class="text-xl font-semibold text-gray-900 mb-2">
								4 on-line lectures with a teacher
							</h5>
							<p class="text-gray-600">
								Quisque eget porta mauris. Praesent eu tincidunt nulla, suscipit
								lobortis est.
							</p>
						</div>
					</div>

					<!-- Step 2 -->
					<div class="flex gap-4" data-aos="fade-up" data-aos-delay="50">
						<div class="flex-shrink-0">
							<div
								class="flex items-center justify-center h-10 w-10 rounded-full bg-gradient-to-br from-[#ff0844] to-[#ff8b67]"
							>
								<i class="icon-check icon text-white text-lg"></i>
							</div>
						</div>
						<div>
							<h5 class="text-xl font-semibold text-gray-900 mb-2">
								Subscription gives access to education materials and videos
							</h5>
							<p class="text-gray-600">
								Quisque eget porta mauris. Praesent eu tincidunt nulla, suscipit
								lobortis est.
							</p>
						</div>
					</div>

					<!-- Step 3 -->
					<div class="flex gap-4" data-aos="fade-up" data-aos-delay="100">
						<div class="flex-shrink-0">
							<div
								class="flex items-center justify-center h-10 w-10 rounded-full bg-gradient-to-br from-[#ff0844] to-[#ff8b67]"
							>
								<i class="icon-check icon text-white text-lg"></i>
							</div>
						</div>
						<div>
							<h5 class="text-xl font-semibold text-gray-900">
								After completing the course and completing the tasks, you will
								receive a certificate
							</h5>
						</div>
					</div>
				</div>

				<!-- Right - Review Card -->
				<div class="flex items-center justify-center" data-aos="zoom-in">
					<div
						class="bg-white rounded-xl p-8 shadow-lg text-center w-full max-w-md"
					>
						<div class="w-24 h-24 mx-auto mb-4 rounded-full overflow-hidden">
							<img
								src="/img/bg.png"
								alt="Review author"
								class="w-full h-full object-cover"
							/>
						</div>
						<h5 class="text-xl font-semibold text-gray-900 mb-3">
							Diana Gloster
						</h5>
						<div class="flex justify-center gap-1 mb-4">
							<i
								v-for="i in 5"
								:key="i"
								class="icon-star icon text-[#f83600]"
							></i>
						</div>
						<p class="text-gray-600 text-lg italic">
							"Mauris tellus lorem, tempus sed nibh at, varius convallis mi. sed
							scelerisque odio neque a lacus. Ut consectetur ligula. ed rhoncus
							sapien eget feugiat."
						</p>
					</div>
				</div>
			</div>
		</div>
	</section>

	<!-- Popular Courses Section -->
	<section class="py-20 px-5 lg:py-32">
		<div class="max-w-[1200px] mx-auto">
			<!-- Header -->
			<div class="text-center mb-12">
				<h2
					class="text-4xl md:text-5xl font-bold text-gray-900 mb-6"
					data-aos="fade-up"
				>
					Popular courses
				</h2>
				<p class="text-gray-600 text-lg max-w-2xl mx-auto" data-aos="fade-down">
					Sed a eros sodales diam sagittis faucibus. Cras id erat nisl. Fusce
					faucibus nulla sed finibus egestas. Vestibulum purus magna.
				</p>
			</div>

			<!-- Tags -->
			<div class="flex flex-wrap justify-center gap-3 mb-16" data-aos="fade-up">
				<button
					class="px-6 py-2 border-2 border-gray-300 rounded-full text-gray-700 font-semibold hover:bg-gray-900 hover:text-white hover:border-gray-900 transition-all duration-300"
				>
					programming
				</button>
				<button
					class="px-6 py-2 border-2 border-gray-300 rounded-full text-gray-700 font-semibold hover:bg-gray-900 hover:text-white hover:border-gray-900 transition-all duration-300"
				>
					management
				</button>
				<button
					class="px-6 py-2 border-2 border-gray-300 rounded-full text-gray-700 font-semibold hover:bg-gray-900 hover:text-white hover:border-gray-900 transition-all duration-300"
				>
					art
				</button>
				<button
					class="px-6 py-2 border-2 border-gray-300 rounded-full text-gray-700 font-semibold hover:bg-gray-900 hover:text-white hover:border-gray-900 transition-all duration-300"
				>
					digital marketing
				</button>
				<button
					class="px-6 py-2 border-2 border-gray-300 rounded-full text-gray-700 font-semibold hover:bg-gray-900 hover:text-white hover:border-gray-900 transition-all duration-300"
				>
					game development
				</button>
				<button
					class="px-6 py-2 border-2 border-gray-300 rounded-full text-gray-700 font-semibold hover:bg-gray-900 hover:text-white hover:border-gray-900 transition-all duration-300"
				>
					smm
				</button>
			</div>

			<!-- Courses Grid -->
			<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
				<!-- Course Card 1 -->
				<div
					class="bg-white rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl hover:-translate-y-3 transition-all duration-300 group"
					data-aos="fade-up"
				>
					<div class="p-8 flex flex-col h-full">
						<!-- Top Section -->
						<div class="mb-6">
							<div class="flex gap-4 mb-4">
								<div
									class="w-20 h-20 bg-gradient-to-br from-purple-600 to-blue-600 rounded-xl flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform duration-300"
								>
									<i class="icon-code-solid icon text-white text-3xl"></i>
								</div>
								<div class="flex-1">
									<h5
										class="text-2xl font-bold text-gray-900 mb-2 group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-purple-600 group-hover:to-blue-600 transition-all duration-300"
									>
										Computer Programming Basic
									</h5>
									<div class="flex gap-1 mb-2">
										<i
											v-for="i in 5"
											:key="i"
											class="icon-star icon text-[#f83600]"
										></i>
									</div>
									<p class="text-sm text-gray-600">by Adrian Dawson school</p>
									<p class="text-sm font-bold text-blue-600">
										48 lectures ( 280 Hours)
									</p>
								</div>
							</div>
						</div>

						<!-- Pricing -->
						<div class="bg-blue-50 p-4 rounded-lg mb-6 text-center">
							<p class="text-xl font-bold text-gray-900">
								$120 all course / $20 per month
							</p>
						</div>

						<!-- Features -->
						<div class="space-y-3 mb-6 flex-1">
							<div class="flex gap-2">
								<span class="text-blue-600 text-xl flex-shrink-0">•</span>
								<p class="text-gray-600 text-sm">
									Mauris tellus lorem, tempus sed nibh at, varius convallis mi
								</p>
							</div>
							<div class="flex gap-2">
								<span class="text-blue-600 text-xl flex-shrink-0">•</span>
								<p class="text-gray-600 text-sm">
									Aenean tristique sodales enim, et consequat velit. Morbi sit
									amet lorem sapien
								</p>
							</div>
						</div>

						<!-- Button -->
						<a
							href="#"
							class="w-full bg-white border-2 border-blue-600 text-blue-600 font-bold py-3 rounded-lg hover:bg-blue-600 hover:text-white transition-all duration-300 flex items-center justify-center gap-2 group/btn"
						>
							<span>SIGN UP FOR A COURSE</span>
							<i
								class="icon-arrow-right-solid icon text-lg group-hover/btn:translate-x-1 transition-transform duration-300"
							></i>
						</a>
					</div>
				</div>

				<!-- Course Card 2 -->
				<div
					class="bg-white rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl hover:-translate-y-3 transition-all duration-300 group"
					data-aos="fade-up"
					data-aos-delay="50"
				>
					<div class="p-8 flex flex-col h-full">
						<div class="mb-6">
							<div class="flex gap-4 mb-4">
								<div
									class="w-20 h-20 bg-gradient-to-br from-orange-500 to-red-600 rounded-xl flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform duration-300"
								>
									<i class="icon-css3 icon text-white text-3xl"></i>
								</div>
								<div class="flex-1">
									<h5
										class="text-2xl font-bold text-gray-900 mb-2 group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-orange-500 group-hover:to-red-600 transition-all duration-300"
									>
										Computer CSS3 Programming
									</h5>
									<div class="flex gap-1 mb-2">
										<i
											v-for="i in 5"
											:key="i"
											class="icon-star icon text-[#f83600]"
										></i>
									</div>
									<p class="text-sm text-gray-600">by Adrian Dawson school</p>
									<p class="text-sm font-bold text-blue-600">
										48 lectures ( 280 Hours)
									</p>
								</div>
							</div>
						</div>
						<div class="bg-blue-50 p-4 rounded-lg mb-6 text-center">
							<p class="text-xl font-bold text-gray-900">
								$120 all course / $20 per month
							</p>
						</div>
						<div class="space-y-3 mb-6 flex-1">
							<div class="flex gap-2">
								<span class="text-blue-600 text-xl flex-shrink-0">•</span>
								<p class="text-gray-600 text-sm">
									Mauris tellus lorem, tempus sed nibh at, varius convallis mi
								</p>
							</div>
							<div class="flex gap-2">
								<span class="text-blue-600 text-xl flex-shrink-0">•</span>
								<p class="text-gray-600 text-sm">
									Aenean tristique sodales enim, et consequat velit. Morbi sit
									amet lorem sapien
								</p>
							</div>
						</div>
						<a
							href="#"
							class="w-full bg-white border-2 border-blue-600 text-blue-600 font-bold py-3 rounded-lg hover:bg-blue-600 hover:text-white transition-all duration-300 flex items-center justify-center gap-2 group/btn"
						>
							<span>SIGN UP FOR A COURSE</span>
							<i
								class="icon-arrow-right-solid icon text-lg group-hover/btn:translate-x-1 transition-transform duration-300"
							></i>
						</a>
					</div>
				</div>

				<!-- Course Card 3 -->
				<div
					class="bg-white rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl hover:-translate-y-3 transition-all duration-300 group"
					data-aos="fade-up"
					data-aos-delay="100"
				>
					<div class="p-8 flex flex-col h-full">
						<div class="mb-6">
							<div class="flex gap-4 mb-4">
								<div
									class="w-20 h-20 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-xl flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform duration-300"
								>
									<i class="icon-sitemap-solid icon text-white text-3xl"></i>
								</div>
								<div class="flex-1">
									<h5
										class="text-2xl font-bold text-gray-900 mb-2 group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-cyan-500 group-hover:to-blue-600 transition-all duration-300"
									>
										Web-site Development Pro
									</h5>
									<div class="flex gap-1 mb-2">
										<i
											v-for="i in 5"
											:key="i"
											class="icon-star icon text-[#f83600]"
										></i>
									</div>
									<p class="text-sm text-gray-600">by Adrian Dawson school</p>
									<p class="text-sm font-bold text-blue-600">
										48 lectures ( 280 Hours)
									</p>
								</div>
							</div>
						</div>
						<div class="bg-blue-50 p-4 rounded-lg mb-6 text-center">
							<p class="text-xl font-bold text-gray-900">
								$120 all course / $20 per month
							</p>
						</div>
						<div class="space-y-3 mb-6 flex-1">
							<div class="flex gap-2">
								<span class="text-blue-600 text-xl flex-shrink-0">•</span>
								<p class="text-gray-600 text-sm">
									Mauris tellus lorem, tempus sed nibh at, varius convallis mi
								</p>
							</div>
							<div class="flex gap-2">
								<span class="text-blue-600 text-xl flex-shrink-0">•</span>
								<p class="text-gray-600 text-sm">
									Aenean tristique sodales enim, et consequat velit. Morbi sit
									amet lorem sapien
								</p>
							</div>
						</div>
						<a
							href="#"
							class="w-full bg-white border-2 border-blue-600 text-blue-600 font-bold py-3 rounded-lg hover:bg-blue-600 hover:text-white transition-all duration-300 flex items-center justify-center gap-2 group/btn"
						>
							<span>SIGN UP FOR A COURSE</span>
							<i
								class="icon-arrow-right-solid icon text-lg group-hover/btn:translate-x-1 transition-transform duration-300"
							></i>
						</a>
					</div>
				</div>
			</div>

			<!-- Learn More Button -->
			<div class="flex justify-center" data-aos="fade-up">
				<a
					href="#"
					class="bg-gradient-to-br from-[#ff0844] to-[#ff8b67] text-white font-bold uppercase px-12 py-4 rounded-xl hover:shadow-lg transition-all duration-300"
				>
					Learn More
				</a>
			</div>
		</div>
	</section>

	<Streak v-model="showStreakModal" :streakInfo="streakInfo" />
</template>

<script setup lang="ts">
import { computed, inject, onMounted, ref } from 'vue'
import { call, createResource, TabButtons, usePageMeta } from 'frappe-ui'
import { sessionStore } from '@/stores/session'
import Streak from '@/pages/Home/Streak.vue'

const user = inject<any>('$user')
const { brand } = sessionStore()
const evalCount = ref(0)
const currentTab = ref<'student' | 'instructor'>('instructor')
const showStreakModal = ref(false)

onMounted(() => {
	call('lms.lms.utils.get_upcoming_evals')
		.then((data: any) => {
			evalCount.value = data.length
		})
		.catch((err) => console.error('Error fetching evals:', err))
})

const isAdmin = computed(() => {
	return (
		user.data?.is_moderator ||
		user.data?.is_instructor ||
		user.data?.is_evaluator
	)
})

const myLiveClasses = createResource({
	url: 'lms.lms.utils.get_my_live_classes',
	auto: !isAdmin.value ? true : false,
})

const adminLiveClasses = createResource({
	url: 'lms.lms.utils.get_admin_live_classes',
	auto: isAdmin.value ? true : false,
})

const adminEvals = createResource({
	url: 'lms.lms.utils.get_admin_evals',
	auto: isAdmin.value ? true : false,
})

const streakInfo = createResource({
	url: 'lms.lms.utils.get_streak_info',
	auto: true,
})

const subtitle = computed(() => {
	if (isAdmin.value) {
		let liveClassSuffix =
			adminLiveClasses.data?.length > 1 ? __('live classes') : __('live class')
		let evalSuffix =
			adminEvals.data?.length > 1 ? __('evaluations') : __('evaluation')
		if (adminLiveClasses.data?.length > 0 && adminEvals.data?.length > 0) {
			return __('You have {0} upcoming {1} and {2} {3} scheduled.').format(
				adminLiveClasses.data.length,
				liveClassSuffix,
				adminEvals.data.length,
				evalSuffix,
			)
		} else if (adminLiveClasses.data?.length > 0) {
			return __('You have {0} upcoming {1}.').format(
				adminLiveClasses.data.length,
				liveClassSuffix,
			)
		} else if (adminEvals.data?.length > 0) {
			return __('You have {0} {1} scheduled.').format(
				adminEvals.data.length,
				evalSuffix,
			)
		}
		return __('Manage your courses and batches at a glance')
	} else {
		let liveClassSuffix =
			myLiveClasses.data?.length > 1 ? __('live classes') : __('live class')
		let evalSuffix = evalCount.value > 1 ? __('evaluations') : __('evaluation')
		if (myLiveClasses.data?.length > 0 && evalCount.value > 0) {
			return __('You have {0} upcoming {1} and {2} {3} scheduled.').format(
				myLiveClasses.data.length,
				liveClassSuffix,
				evalCount.value,
				evalSuffix,
			)
		} else if (myLiveClasses.data?.length > 0) {
			return __('You have {0} upcoming {1}.').format(
				myLiveClasses.data.length,
				liveClassSuffix,
			)
		} else if (evalCount.value > 0) {
			return __('You have {0} {1} scheduled.').format(
				evalCount.value,
				evalSuffix,
			)
		}
		return __('Resume where you left off')
	}
})

const tabs = [
	{ label: __('Student'), value: 'student' },
	{ label: __('Instructor'), value: 'instructor' },
]

usePageMeta(() => {
	return {
		title: __('Home'),
		icon: brand.favicon,
	}
})
</script>
