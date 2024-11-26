import os
import random
import sys
import pygame as pg
import time

WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数:で与えられたRCTが画面の中か外かを判定する関数
    引数:こうかとんRect or 爆弾Rect
    戻り値:真理値タプル(横, 縦) True:画面内 False:画面外
    """
    yoko, tate = True, True
    if rct.left < 0 or rct.right > WIDTH:  # 横方向判定
        yoko = False
    if rct.top < 0 or rct.bottom > HEIGHT:  # 縦方向判定
        tate = False
    return yoko, tate


def show_game_over(screen, kk_img, font):
    """ゲームオーバー画面を表示する"""
    # 画面をブラックアウト
    overlay = pg.Surface((WIDTH, HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(150)  # 半透明

    # 泣いているこうかとんの画像
    crying_kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)

    # ゲームオーバー文字
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    spacing = 20  # 文字と画像の間の間隔
    left_kk_rect = crying_kk_img.get_rect(midright=(text_rect.left - spacing, HEIGHT // 2))
    right_kk_rect = crying_kk_img.get_rect(midleft=(text_rect.right + spacing, HEIGHT // 2))

    # 画面描画
    screen.blit(overlay, (0, 0))
    screen.blit(text, text_rect)
    screen.blit(crying_kk_img, left_kk_rect)
    screen.blit(crying_kk_img, right_kk_rect)
    pg.display.update()

    # 5秒間停止
    time.sleep(5)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  # 爆弾用の空surface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 爆弾円を描く
    bb_img.set_colorkey((0, 0, 0))  # 黒色を透明化
    bb_rct = bb_img.get_rect()  # 爆弾のrectの抽出
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)  # 爆弾の初期位置
    vx, vy = +5, +5  # 爆弾の速度ベクトル
    clock = pg.time.Clock()
    tmr = 0
    font = pg.font.Font(None, 80)  # ゲームオーバー用フォント

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        if kk_rct.colliderect(bb_rct):
            show_game_over(screen, kk_img, font)
            return  # ゲームオーバー

        screen.blit(bg_img, [0, 0])

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)
        # こうかとんが画面外なら、元の場所に戻す
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
