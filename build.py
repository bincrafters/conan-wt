#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bincrafters import build_template_default


def add_build_requires(builds):
    return map(add_required_installers, builds)


def add_required_installers(build):
    installers = ['ninja/1.9.0']
    build.build_requires.update({"*": installers})
    return build


if __name__ == "__main__":

    builder = build_template_default.get_builder(pure_c=False)

    filtered_builds = []
    for settings, options, env_vars, build_requires, reference in builder.items:
        if settings['compiler'] == 'gcc' and float(settings['compiler.version']) >= 5:
            if settings['compiler.libcxx'] == 'libstdc++11':
                filtered_builds.append([settings, options, env_vars, build_requires])
        elif settings['compiler'] == 'clang':
            if settings['compiler.libcxx'] == 'libstdc++11' or settings['compiler.libcxx'] == 'libc++':
                filtered_builds.append([settings, options, env_vars, build_requires])
        else:
            filtered_builds.append([settings, options, env_vars, build_requires])
    builder.builds = filtered_builds

    builder.run()
