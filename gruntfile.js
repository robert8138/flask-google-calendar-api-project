module.exports = function(grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        watch: {
            src: {
                files: ['src/templates/*.html', 'src/static/css/*.css'],
                options: { livereload: true }
            }
        }
    });
    grunt.loadNpmTasks('grunt-contrib-watch');
};